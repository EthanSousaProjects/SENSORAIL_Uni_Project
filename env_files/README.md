# Environment Files Dev note

- If another package needs to be added to the generic conda environment make sure you add it to both the `generic_conda_env.yml` file and the `pi_conda_env.yml`.

- If a package needs to be added to only the raspberry pi (like gpiozero) make sure to input the package and version into the `pi_conda_env.yml` file.

- We have tried to use all the packages from the conda forge as it has more than the generic conda channel. However not all packages are avaliable in conda forge so pip packages can also be used and added to this env file.

- Pip packages must be at the bottom of the packages to import. All conda packages should come before the pip commands in the env file.