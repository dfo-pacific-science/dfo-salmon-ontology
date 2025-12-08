{ pkgs, lib, ... }:

let
  basePackages = with pkgs; [
    git
    jq
    ripgrep
    fd
    tree
    pre-commit
    direnv
    python3
    python3Packages.rdflib
    python3Packages.pypdf
    nodejs_22
    jdk21_headless
  ] ++ lib.optionals pkgs.stdenv.isDarwin [ coreutils ];
in {
  # Base CLI tools - extend per-project below
  packages = basePackages ++ lib.optionals (pkgs ? robot) [ pkgs.robot ];

  # Optional language presets (uncomment per project)
  # Python data science stack
  # languages.python = {
  #   enable = true;
  #   package = pkgs.python3;
  #   venv = {
  #     enable = true;
  #     requirements = ./requirements.txt;
  #   };
  # };

  # Node.js stack
  # languages.javascript = {
  #   enable = true;
  #   package = pkgs.nodejs_22;
  #   npm.install.enable = true;
  # };

  # R stack
  # languages.r = {
  #   enable = true;
  #   package = pkgs.rWrapper.override {
  #     packages = with pkgs.rPackages; [
  #       readr
  #       jsonlite
  #       yaml
  #       dplyr
  #       tidyr
  #       tibble
  #       purrr
  #     ];
  #   };
  # };

  enterShell = ''
    echo "==========================================="
    echo " Devenv Shell (Template Base)"
    echo "==========================================="
    echo "System: $(uname -a)"
    echo "Python version: $(python --version 2>/dev/null || echo 'python not available')"
    echo "Node version: $(node --version 2>/dev/null || echo 'node not available')"
    echo ""
    echo "Core conventions:"
    echo "  - Devenv provides a declarative dev environment (standalone, no flake needed)."
    echo "  - Add packages in devenv.nix packages list."
    echo "  - Enable language support in devenv.nix (uncomment as needed)."
    echo "  - Language-specific managers handle app-specific deps."
    echo "  - Use pre-commit (installed by devenv) for hooks: pre-commit install"
    echo ""
  '';

  # Pre-commit hooks (optional - uncomment to enable)
  # pre-commit.hooks = {
  #   nixfmt.enable = true;
  #   shellcheck.enable = true;
  # };
}
