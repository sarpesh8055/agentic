
import requests
from packaging.requirements import Requirement
from packaging.version import Version

def main():
    checked = 0
    missing_packages = []
    missing_versions = []
    pinned = []

    with open("requirements.txt", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#") or line.startswith("-"):
                continue

            try:
                req = Requirement(line)
            except Exception:
                continue

            name = req.name
            version = next(
                (s.version for s in req.specifier
                 if s.operator == "=="),
                None
            )
            checked += 1

            try:
                response = requests.get(
                    f"https://pypi.org/pypi/{name}/json",
                    timeout=15
                )

                if response.status_code == 404:
                    missing_packages.append(name)
                    continue

                response.raise_for_status()
                releases = response.json()["releases"]

                if version:
                    if version not in releases or not releases[version]:
                        missing_versions.append(f"{name}=={version}")
                    else:
                        pinned.append((Version(version), name, version))

            except requests.RequestException as error:
                print(f"Could not check {name}: {error}")

    print("\nDependencies checked:", checked)

    print("\nPackages not on PyPI:")
    print("\n".join(missing_packages) if missing_packages else "None")

    print("\nVersions not on PyPI:")
    print("\n".join(missing_versions) if missing_versions else "None")

    print("\nOldest pinned release:")
    if pinned:
        oldest = min(pinned)
        print(f"{oldest[1]}=={oldest[2]}")
    else:
        print("None")
    
    print("\n========== DEPENDENCY REPORT ==========")
    print(f"Dependencies checked: {checked}")
    print(f"Packages not on PyPI: {len(missing_packages)}")
    print(f"Versions not on PyPI: {len(missing_versions)}")

    print("\nOldest pinned release:")
    if pinned:
        oldest = min(pinned)
        print(f"{oldest[1]}=={oldest[2]}")
    else:
        print("None")



if __name__ == "__main__":
    main()
