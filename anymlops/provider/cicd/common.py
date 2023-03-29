import os


def pip_install_anymlops(anymlops_version: str) -> str:
    anymlops_gh_branch = os.environ.get("ANYMLOPS_GH_BRANCH", None)
    pip_install = f"pip install anymlops=={anymlops_version}"
    # dev branches
    if anymlops_gh_branch:
        pip_install = f"pip install git+https://github.com/anymlops-dev/anymlops.git@{anymlops_gh_branch}"

    return pip_install
