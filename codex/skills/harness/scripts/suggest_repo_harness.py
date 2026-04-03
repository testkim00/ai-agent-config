#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None

EXCLUDED_PARTS = {
    ".git",
    "node_modules",
    ".nuxt",
    ".next",
    "dist",
    "build",
    "target",
    "bin",
    "obj",
    ".venv",
    "venv",
    "__pycache__",
}
PRESETS_DIR = Path(__file__).resolve().parents[1] / "presets"
CONSISTENCY_DISABLED_REPO_NAMES = {"WooriApiManagement", "ApiHub"}

MANDATORY_CONSISTENCY_CHECKS = [
    "같은 계열 기존 화면(혹은 API) 2~3개를 reference로 잡았는지",
    "최대한 기존의 공통 wrapper/layout/component/module 등을 활용하는지",
    "inline color, inline spacing, local-only radius 같은 임의 스타일을 넣지 않았는지",
    "(shared) component import 패턴이 기존과 맞는지",
    "grid/list/form 화면별로 정해둔 기본 구조를 벗어났는지",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Suggest a repo-specific .codex/harness.json")
    parser.add_argument("--repo", required=True, help="Target repository root")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Output format")
    return parser.parse_args()


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


def read_toml(path: Path):
    if tomllib is None:
        return None
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


def load_preset(name: str) -> Dict[str, object]:
    path = PRESETS_DIR / f"{name}.json"
    payload = read_json(path)
    if not isinstance(payload, dict):
        raise RuntimeError(f"invalid preset: {path}")
    return payload


def has_any_files(repo: Path, patterns: List[str]) -> bool:
    for pattern in patterns:
        for path in repo.glob(pattern):
            relative_parts = set(path.relative_to(repo).parts)
            if relative_parts & EXCLUDED_PARTS:
                continue
            return True
    return False


def iter_repo_files(repo: Path, patterns: List[str]):
    for pattern in patterns:
        for path in repo.glob(pattern):
            relative_parts = set(path.relative_to(repo).parts)
            if relative_parts & EXCLUDED_PARTS:
                continue
            yield path


def repo_file_contains(repo: Path, patterns: List[str], needles: List[str]) -> bool:
    lowered_needles = [needle.lower() for needle in needles]
    for path in iter_repo_files(repo, patterns):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
        except Exception:  # noqa: BLE001
            continue
        if any(needle in text for needle in lowered_needles):
            return True
    return False


def detect_node(repo: Path) -> Tuple[Set[str], List[str]]:
    tags: Set[str] = set()
    reasons: List[str] = []
    package_json = repo / "package.json"
    if not package_json.exists():
        return tags, reasons

    payload = read_json(package_json)
    scripts = payload.get("scripts", {}) if isinstance(payload, dict) else {}
    if not isinstance(scripts, dict):
        scripts = {}

    reasons.append("Detected Node repo via package.json")
    if "lint" in scripts:
        tags.add("lint")
        reasons.append("package.json exposes lint")
    if "typecheck" in scripts or has_any_files(repo, ["tsconfig.json", "tsconfig.*.json"]):
        tags.add("typecheck")
        reasons.append("TypeScript or typecheck signal detected")
    if "test" in scripts:
        tags.add("test")
        reasons.append("package.json exposes test")
    if "build" in scripts:
        tags.add("build")
        reasons.append("package.json exposes build")
    if "check" in scripts:
        tags.add("check")
        reasons.append("package.json exposes check")
    return tags, reasons


def detect_python(repo: Path) -> Tuple[Set[str], List[str]]:
    tags: Set[str] = set()
    reasons: List[str] = []
    pyproject = repo / "pyproject.toml"
    requirements = repo / "requirements.txt"
    if not pyproject.exists() and not requirements.exists() and not has_any_files(repo, ["**/*.py"]):
        return tags, reasons

    reasons.append("Detected Python signal")
    payload = read_toml(pyproject) if pyproject.exists() else None
    text = pyproject.read_text(encoding="utf-8") if pyproject.exists() else ""
    if "ruff" in text or "flake8" in text or "pylint" in text:
        tags.add("lint")
        reasons.append("Python lint tool detected")
    if "mypy" in text or "pyright" in text or "pytype" in text:
        tags.add("typecheck")
        reasons.append("Python typecheck tool detected")
    if "pytest" in text or (requirements.exists() and "pytest" in requirements.read_text(encoding="utf-8")):
        tags.add("test")
        reasons.append("pytest detected")
    if has_any_files(repo, ["**/*.py"]):
        tags.add("check")
        reasons.append("Python source exists, py_compile is a cheap fallback")
    _ = payload
    return tags, reasons


def detect_dotnet(repo: Path) -> Tuple[Set[str], List[str]]:
    tags: Set[str] = set()
    reasons: List[str] = []
    if not has_any_files(repo, ["*.sln", "**/*.csproj"]):
        return tags, reasons
    tags.update({"build", "test"})
    reasons.append("Detected .NET solution/project files")
    return tags, reasons


def detect_go(repo: Path) -> Tuple[Set[str], List[str]]:
    tags: Set[str] = set()
    reasons: List[str] = []
    if not (repo / "go.mod").exists():
        return tags, reasons
    tags.update({"test", "build"})
    reasons.append("Detected Go module")
    if has_any_files(repo, [".golangci.yml", ".golangci.yaml"]):
        tags.add("lint")
        reasons.append("golangci-lint config detected")
    return tags, reasons


def detect_rust(repo: Path) -> Tuple[Set[str], List[str]]:
    tags: Set[str] = set()
    reasons: List[str] = []
    if not (repo / "Cargo.toml").exists():
        return tags, reasons
    tags.update({"check", "test"})
    reasons.append("Detected Rust crate")
    return tags, reasons


def detect_java(repo: Path) -> Tuple[Set[str], List[str]]:
    tags: Set[str] = set()
    reasons: List[str] = []
    if not (repo / "pom.xml").exists() and not has_any_files(repo, ["build.gradle", "build.gradle.kts"]):
        return tags, reasons
    tags.update({"build", "test"})
    reasons.append("Detected Java/Maven/Gradle build files")
    return tags, reasons


def detect_shell(repo: Path) -> Tuple[Set[str], List[str]]:
    tags: Set[str] = set()
    reasons: List[str] = []
    if not has_any_files(repo, ["**/*.sh", "**/*.bash", "**/*.zsh"]):
        return tags, reasons
    tags.update({"check"})
    reasons.append("Detected shell scripts, sh -n is a cheap validation")
    return tags, reasons


def detect_docs_only(repo: Path) -> bool:
    code_patterns = [
        "**/*.py",
        "**/*.ts",
        "**/*.tsx",
        "**/*.js",
        "**/*.jsx",
        "**/*.cs",
        "**/*.go",
        "**/*.rs",
        "**/*.java",
        "**/*.kt",
        "**/*.sh",
        "**/*.bash",
        "**/*.zsh",
    ]
    return not has_any_files(repo, code_patterns)


def append_unique(items: List[str], *values: str) -> None:
    for value in values:
        if value and value not in items:
            items.append(value)


def package_scripts(repo: Path) -> Dict[str, str]:
    payload = read_json(repo / "package.json")
    scripts = payload.get("scripts", {}) if isinstance(payload, dict) else {}
    return scripts if isinstance(scripts, dict) else {}


def package_dependencies(repo: Path) -> Set[str]:
    payload = read_json(repo / "package.json")
    if not isinstance(payload, dict):
        return set()
    dependencies = payload.get("dependencies", {})
    dev_dependencies = payload.get("devDependencies", {})
    dep_names: Set[str] = set()
    if isinstance(dependencies, dict):
        dep_names.update(dependencies)
    if isinstance(dev_dependencies, dict):
        dep_names.update(dev_dependencies)
    return dep_names


def runner_regex(script_name: str) -> str:
    return rf"command:(^|\s)(?:npm|pnpm|yarn|bun)\s+(?:run\s+)?{re.escape(script_name)}\b"


def looks_like_noop_test(script_value: str) -> bool:
    lowered = script_value.lower()
    return "no test specified" in lowered and "exit 0" in lowered


def is_winforms_repo(repo: Path) -> bool:
    return repo_file_contains(
        repo,
        ["**/*.csproj", "**/*.vbproj", "**/*.cs"],
        [
            "usewindowsforms",
            "system.windows.forms",
            "<subtype>form</subtype>",
            "<outputtype>winexe</outputtype>",
            "initializecomponent(",
        ],
    )


def is_legacy_dotnet_repo(repo: Path) -> bool:
    return repo_file_contains(
        repo,
        ["**/*.csproj", "**/*.vbproj"],
        [
            "<targetframeworkversion>",
            "toolsversion=\"",
        ],
    )


def has_dotnet_test_project(repo: Path) -> bool:
    return repo_file_contains(
        repo,
        ["**/*.csproj", "**/*.vbproj", "**/packages.config"],
        [
            "microsoft.net.test.sdk",
            "<istestproject>true</istestproject>",
            "xunit",
            "nunit",
            "mstest.testframework",
            "microsoft.visualstudio.testtools.unittesting",
        ],
    )


def build_consistency_check(repo: Path) -> Dict[str, object]:
    repo_name = repo.name
    repo_name_lower = repo_name.lower()
    dependencies = package_dependencies(repo)
    has_frontend = bool(
        dependencies & {"quasar", "@quasar/app-vite", "nuxt", "vue", "react", "next", "vite"}
    ) or has_any_files(repo, ["src/**/*.vue", "pages/**/*.vue", "layouts/**/*.vue", "components/**/*.vue"])
    has_dotnet = has_any_files(repo, ["*.sln", "**/*.csproj"])
    has_java = (repo / "pom.xml").exists() or has_any_files(repo, ["build.gradle", "build.gradle.kts"])
    has_go = (repo / "go.mod").exists()
    has_python = (repo / "pyproject.toml").exists() or (repo / "requirements.txt").exists() or has_any_files(repo, ["**/*.py"])
    has_winforms = is_winforms_repo(repo)

    if repo_name == "ai-agent-config":
        return {
            "enabled": True,
            "profile": "tooling-config",
            "summary": (
                "ai-agent-config는 Codex/Claude 설정, skill, hook, script를 다루는 tooling repo라서 "
                "기존 skill/workflow/module 패턴과 파일 배치를 먼저 맞춘다."
            ),
            "applies_to": [
                "codex/**/*.md",
                "codex/**/*.py",
                ".codex/**/*.json",
                ".codex/**/*.py",
                "**/*.sh",
            ],
            "reference_expectation": (
                "최종 보고에서 참고한 기존 skill/script/module 2~3개와 재사용한 helper/template를 짧게 남긴다."
            ),
            "required_checklist": MANDATORY_CONSISTENCY_CHECKS,
            "project_notes": [
                "이 repo에서는 화면/API보다 skill, hook, script, config module의 책임 분리와 command 흐름 일관성이 더 중요하다.",
                "공통 runner, template, helper module이 있으면 새 파일 구조보다 기존 조합과 naming을 우선한다.",
                "UI 관련 체크 항목은 frontend artifact나 web skill 산출물을 실제로 수정할 때만 직접 적용하고, 그 외에는 command/module 구조에 대응시켜 해석한다.",
            ],
        }

    if has_frontend:
        if "nuxt" in dependencies:
            stack_label = "Nuxt/Vue"
        elif "quasar" in dependencies or "@quasar/app-vite" in dependencies:
            stack_label = "Quasar/Vue"
        elif "react" in dependencies:
            stack_label = "React"
        else:
            stack_label = "frontend"

        scope_label = "화면/페이지"
        if "portal" in repo_name_lower:
            scope_label = "포털 화면"
        elif "client" in repo_name_lower or "ui" in repo_name_lower:
            scope_label = "업무 화면"

        return {
            "enabled": True,
            "profile": "frontend-screen",
            "summary": (
                f"{repo_name}는 {stack_label} 기반 {scope_label} repo라서 기존 page shell, layout, shared component, "
                "list/form 패턴을 먼저 맞춘다."
            ),
            "applies_to": [
                "src/**/*.vue",
                "src/**/*.ts",
                "src/**/*.js",
                "src/**/*.scss",
                "src/**/*.sass",
                "src/**/*.css",
            ],
            "reference_expectation": (
                "최종 보고에서 참고한 기존 화면/컴포넌트 2~3개와 재사용한 wrapper/layout/component/module을 짧게 남긴다."
            ),
            "required_checklist": MANDATORY_CONSISTENCY_CHECKS,
            "project_notes": [
                "같은 메뉴군의 기존 page, popup, table, form 2~3개를 먼저 읽고 header/search/filter/body 배치를 최대한 맞춘다.",
                "공통 page shell, dialog wrapper, form/grid component, shared module이 있으면 새 마크업보다 기존 조합을 우선한다.",
                "새 화면을 만들더라도 spacing, color token, radius, import 순서, section naming은 인접한 기존 화면의 패턴을 그대로 따른다.",
            ],
        }

    if has_winforms:
        return {
            "enabled": True,
            "profile": "desktop-winforms",
            "summary": (
                f"{repo_name}는 legacy WinForms/desktop repo라서 기존 Form, Designer, BaseForm, popup, grid 배치를 먼저 맞춘다."
            ),
            "applies_to": [
                "**/*.cs",
                "**/*.Designer.cs",
                "**/*.resx",
                "**/*.csproj",
            ],
            "reference_expectation": (
                "최종 보고에서 참고한 기존 Form/popup/base form 2~3개와 재사용한 공통 control/helper/module을 짧게 남긴다."
            ),
            "required_checklist": MANDATORY_CONSISTENCY_CHECKS,
            "project_notes": [
                "이 repo에서는 API보다 Form, Designer, BaseForm, UserControl, DevExpress grid/layout 패턴이 일관한지가 더 중요하다.",
                "공통 ChildForm/BaseForm, popup shell, grid/search panel, helper module이 있으면 새 화면보다 기존 조합을 우선한다.",
                "새 WinForms 화면을 만들더라도 docking, padding, control naming, event wiring, designer resource 배치는 인접한 기존 화면 패턴을 그대로 따른다.",
            ],
        }

    if has_dotnet or has_java or has_go:
        profile = "backend-api"
        summary = (
            f"{repo_name}는 API/서비스 계층 중심 repo라서 기존 controller/service/module/DTO 구조와 endpoint naming을 먼저 맞춘다."
        )
        if has_dotnet and has_python:
            profile = "mixed-backend-platform"
            summary = (
                f"{repo_name}는 .NET과 Python 보조 자산이 함께 있는 mixed backend repo라서 "
                "변경 범위와 같은 계층의 기존 구현 흐름을 먼저 맞춘다."
            )
        return {
            "enabled": True,
            "profile": profile,
            "summary": summary,
            "applies_to": [
                "**/*.cs",
                "**/*.java",
                "**/*.go",
                "**/*.py",
                "**/*.json",
                "**/*.yml",
                "**/*.yaml",
            ],
            "reference_expectation": (
                "최종 보고에서 참고한 기존 API/controller/service/module 2~3개와 따라간 naming/boundary 규칙을 짧게 남긴다."
            ),
            "required_checklist": MANDATORY_CONSISTENCY_CHECKS,
            "project_notes": [
                "이 repo에서는 화면보다 controller/service/repository/job/module 경계와 request/response DTO 패턴이 일관한지가 더 중요하다.",
                "공통 base class, middleware, helper, mapper, module wiring이 있으면 새 구조보다 기존 조합을 우선한다.",
                "UI 관련 체크 항목은 Swagger/admin/web 자산을 실제로 수정할 때는 그대로 적용하고, 그 외에는 list/detail/create/update/delete API 흐름과 endpoint/module 구조에 대응시켜 해석한다.",
            ],
        }

    if has_python:
        return {
            "enabled": True,
            "profile": "python-service",
            "summary": (
                f"{repo_name}는 Python 서비스/스크립트 중심 repo라서 기존 job/module/service 흐름과 입력·출력 포맷 일관성을 먼저 맞춘다."
            ),
            "applies_to": [
                "**/*.py",
                "**/*.ipynb",
                "**/*.json",
                "**/*.yml",
                "**/*.yaml",
            ],
            "reference_expectation": (
                "최종 보고에서 참고한 기존 service/job/script 2~3개와 재사용한 helper/module을 짧게 남긴다."
            ),
            "required_checklist": MANDATORY_CONSISTENCY_CHECKS,
            "project_notes": [
                "이 repo에서는 화면보다 command/service/job/module 흐름과 입력 파라미터, 결과 포맷, error handling 패턴 일관성이 더 중요하다.",
                "공통 helper, base class, pipeline, serializer가 있으면 새 구현보다 기존 흐름을 우선한다.",
                "UI 관련 체크 항목은 web/admin 자산을 수정할 때만 직접 적용하고, 그 외에는 list/detail/update 배치와 module boundary에 대응시켜 해석한다.",
            ],
        }

    return {
        "enabled": True,
        "profile": "general-module",
        "summary": f"{repo_name}는 공통 module/config 중심 repo라서 기존 디렉터리 배치와 module 책임 분리를 먼저 맞춘다.",
        "applies_to": [
            "**/*",
        ],
        "reference_expectation": (
            "최종 보고에서 참고한 기존 구현 2~3개와 재사용한 공통 module/helper를 짧게 남긴다."
        ),
        "required_checklist": MANDATORY_CONSISTENCY_CHECKS,
        "project_notes": [
            "이 repo에서는 변경 경로와 가장 가까운 기존 구현 2~3개를 먼저 기준으로 잡고 naming, layout, module 배치를 맞춘다.",
            "공통 helper, wrapper, template, module이 있으면 새 구조보다 기존 조합을 우선한다.",
            "UI 관련 체크 항목은 실제 화면 자산을 수정할 때는 그대로 적용하고, 그 외에는 list/detail/update 흐름과 module 구조에 대응시켜 해석한다.",
        ],
    }


def choose_preset_name(repo: Path) -> str:
    repo_name = repo.name
    dependencies = package_dependencies(repo)
    has_frontend = bool(
        dependencies & {"quasar", "@quasar/app-vite", "nuxt", "vue", "react", "next", "vite"}
    ) or has_any_files(repo, ["src/**/*.vue", "pages/**/*.vue", "layouts/**/*.vue", "components/**/*.vue"])

    if repo_name == "ai-agent-config":
        return "tooling-config"
    if has_frontend:
        if "nuxt" in dependencies:
            return "frontend-nuxt"
        if "quasar" in dependencies or "@quasar/app-vite" in dependencies:
            return "frontend-quasar"
        return "frontend-generic"
    if is_winforms_repo(repo):
        return "desktop-winforms"
    if has_any_files(repo, ["*.sln", "**/*.csproj"]):
        return "backend-dotnet"
    if (repo / "go.mod").exists():
        return "go-service"
    if (repo / "pom.xml").exists() or has_any_files(repo, ["build.gradle", "build.gradle.kts"]):
        return "java-service"
    if (repo / "pyproject.toml").exists() or (repo / "requirements.txt").exists() or has_any_files(repo, ["**/*.py"]):
        return "python-service"
    if has_any_files(repo, ["**/*.sh", "**/*.bash", "**/*.zsh"]):
        return "shell-basic"
    return "general-module"


def build_harness(repo: Path) -> Dict[str, object]:
    tags: Set[str] = set()
    reasons: List[str] = []
    docs_only = detect_docs_only(repo)
    required_all: List[str] = []
    required_any: List[str] = []
    scripts = package_scripts(repo)
    preset_name = choose_preset_name(repo)
    preset = load_preset(preset_name)
    has_winforms = is_winforms_repo(repo)
    legacy_dotnet = is_legacy_dotnet_repo(repo)

    if scripts:
        reasons.append("Detected Node repo via package.json")

        lint_script = scripts.get("lint")
        if isinstance(lint_script, str) and lint_script.strip():
            tags.add("lint")
            reasons.append("package.json exposes lint")
            append_unique(required_all, runner_regex("lint"))
            if "eslint" in lint_script.lower():
                append_unique(required_all, r"command:(^|\s)eslint\b")

        typecheck_script = scripts.get("typecheck")
        if isinstance(typecheck_script, str) and typecheck_script.strip():
            tags.add("typecheck")
            reasons.append("package.json exposes typecheck")
            append_unique(required_all, runner_regex("typecheck"))
            if "tsc" in typecheck_script.lower() or "vue-tsc" in typecheck_script.lower():
                append_unique(required_all, r"tag:typecheck")

        build_script = scripts.get("build")
        if isinstance(build_script, str) and build_script.strip():
            tags.add("build")
            reasons.append("package.json exposes build")
            lowered_build = build_script.lower()
            if "quasar" in lowered_build:
                reasons.append("Quasar build detected")
                append_unique(required_any, r"command:quasar(?:\.js)?\s+build\b", runner_regex("build"))
                if "build:pwa" in scripts:
                    append_unique(required_any, runner_regex("build:pwa"))
            elif "nuxt" in lowered_build:
                reasons.append("Nuxt build detected")
                append_unique(required_any, r"command:(^|\s)nuxt\s+build\b", runner_regex("build"))
            else:
                append_unique(required_any, runner_regex("build"), "tag:build")

        test_script = scripts.get("test")
        if isinstance(test_script, str) and test_script.strip() and not looks_like_noop_test(test_script):
            tags.add("test")
            reasons.append("package.json exposes real test")
            append_unique(required_any, runner_regex("test"), "tag:test")

        check_script = scripts.get("check")
        if isinstance(check_script, str) and check_script.strip():
            tags.add("check")
            reasons.append("package.json exposes check")
            append_unique(required_any, runner_regex("check"))

    if has_any_files(repo, ["*.sln", "**/*.csproj"]):
        tags.add("build")
        reasons.append("Detected .NET solution/project files")
        if has_winforms:
            reasons.append("WinForms/Desktop project signal detected")
            reasons.append("Legacy WinForms build validation is not enforced on macOS")
            append_unique(
                required_any,
                r"command:(^|\s)msbuild\b",
                r"command:(^|\s)xbuild\b",
                r"command:(^|\s)(?:devenv|devenv\.com)\b.*\b/build\b",
            )
            if not legacy_dotnet:
                append_unique(required_any, r"command:(^|\s)dotnet\s+build\b")
            if has_dotnet_test_project(repo):
                tags.add("test")
                reasons.append("Detected dedicated .NET test project")
                append_unique(required_any, r"command:(^|\s)dotnet\s+test\b")
        else:
            tags.add("test")
            append_unique(
                required_any,
                r"command:(^|\s)dotnet\s+build\b",
                r"command:(^|\s)dotnet\s+test\b",
                r"command:(^|\s)msbuild\b",
            )

    pyproject = repo / "pyproject.toml"
    requirements = repo / "requirements.txt"
    if pyproject.exists() or requirements.exists() or has_any_files(repo, ["**/*.py"]):
        tags.add("check")
        reasons.append("Detected Python signal")
        pyproject_text = pyproject.read_text(encoding="utf-8") if pyproject.exists() else ""
        requirements_text = requirements.read_text(encoding="utf-8") if requirements.exists() else ""
        if any(tool in pyproject_text for tool in ("ruff", "flake8", "pylint")):
            tags.add("lint")
            reasons.append("Python lint tool detected")
            append_unique(required_all, "tag:lint")
        if any(tool in pyproject_text for tool in ("mypy", "pyright", "pytype")):
            tags.add("typecheck")
            reasons.append("Python typecheck tool detected")
            append_unique(required_all, "tag:typecheck")
        if (
            "pytest" in pyproject_text
            or "pytest" in requirements_text
            or (repo / "pytest.ini").exists()
            or has_any_files(repo, ["tests/**/*.py", "test_*.py"])
        ):
            tags.add("test")
            reasons.append("pytest signal detected")
            append_unique(required_any, r"command:(^|\s)(?:python3?\s+-m\s+)?pytest\b")
        append_unique(
            required_any,
            r"command:(^|\s)python3?\s+-m\s+compileall\b",
            r"command:(^|\s)python3?\s+-m\s+py_compile\b",
        )

    if (repo / "go.mod").exists():
        tags.update({"build", "test"})
        reasons.append("Detected Go module")
        append_unique(required_any, r"command:(^|\s)go\s+test\b", r"command:(^|\s)go\s+build\b")
        if has_any_files(repo, [".golangci.yml", ".golangci.yaml"]):
            tags.add("lint")
            reasons.append("golangci-lint config detected")
            append_unique(required_all, "tag:lint")

    if (repo / "Cargo.toml").exists():
        tags.update({"check", "test"})
        reasons.append("Detected Rust crate")
        append_unique(required_any, r"command:(^|\s)cargo\s+check\b", r"command:(^|\s)cargo\s+test\b")

    if (repo / "pom.xml").exists() or has_any_files(repo, ["build.gradle", "build.gradle.kts"]):
        tags.update({"build", "test"})
        reasons.append("Detected Java/Maven/Gradle build files")
        append_unique(
            required_any,
            r"command:(^|\s)(?:\./)?mvnw?\s+test\b",
            r"command:(^|\s)(?:\./)?mvnw?\s+package\b",
            r"command:(^|\s)(?:\./)?gradlew?\b.*\btest\b",
            r"command:(^|\s)(?:\./)?gradlew?\b.*\bbuild\b",
        )

    if has_any_files(repo, ["**/*.sh", "**/*.bash", "**/*.zsh"]):
        tags.add("check")
        reasons.append("Detected shell scripts")
        if not required_all and not required_any:
            reasons.append("Using shell syntax check as the primary cheap fallback")
            append_unique(required_any, r"command:(^|\s)(?:ba)?sh\s+-n\b")

    if docs_only and not tags:
        enforce = False
        reasons.append("Repo looks docs-only, default enforcement disabled")
    else:
        enforce = True
        if not required_all and not required_any:
            required_any.append("tag:check")
            reasons.append("No clear stack-specific validator found, using generic check fallback")

    harness = {
        "version": 1,
        "preset": preset_name,
        "name": f"{repo.name}-default",
        "description": f"Repo-specific default harness for {repo.name}.",
    }
    reasons.append(f"Selected preset: {preset_name}")

    if enforce != preset.get("enforce", True):
        harness["enforce"] = enforce
    if required_all != preset.get("required_all", []):
        harness["required_all"] = required_all
    if required_any != preset.get("required_any", []):
        harness["required_any"] = required_any
    if repo.name in CONSISTENCY_DISABLED_REPO_NAMES and (
        isinstance(preset.get("consistency_check"), dict) and preset["consistency_check"].get("enabled")
    ):
        harness["consistency_check"] = {"enabled": False}
        reasons.append("Consistency gate intentionally disabled for this repo")
    return {
        "repo_root": str(repo),
        "detected_tags": sorted(tags),
        "reasons": reasons,
        "suggested_harness": harness,
    }


def print_text(result: Dict[str, object]) -> None:
    harness = result["suggested_harness"]
    print(f"repo: {result['repo_root']}")
    print(f"detected_tags: {', '.join(result['detected_tags']) or '-'}")
    print("reasons:")
    for reason in result["reasons"]:
        print(f"- {reason}")
    print("suggested_harness:")
    print(json.dumps(harness, ensure_ascii=False, indent=2))


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).expanduser().resolve()
    if not repo.exists():
        raise SystemExit(f"repo not found: {repo}")
    result = build_harness(repo)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
