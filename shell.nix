{ pkgs ? import <nixpkgs> {}, system ? builtins.currentSystem, }:

# Setup pinned items like dependencies and static env vars.
let
  pinned = import (fetchTarball {
      name = "nixos-23.11";
      url = https://github.com/NixOS/nixpkgs/archive/refs/tags/23.11.tar.gz;
      sha256 = "1ndiv385w1qyb3b18vw13991fzb9wg4cl21wglk89grsfsnra41k";
  }) {};

  google-sdk = pinned.google-cloud-sdk.withExtraComponents( with pinned.google-cloud-sdk.components; [
    gke-gcloud-auth-plugin
  ]);

  bigquery-emulator = pkgs.stdenv.mkDerivation {
    name = "bigquery-emulator";
    version = "0.6.1";

    src = pkgs.fetchurl {
      url = "https://github.com/goccy/bigquery-emulator/releases/download/v0.6.1/bigquery-emulator-linux-amd64";
      sha256 = "sha256-K7ZPWjKv4FLtQeMOw3N2KbYiQDVIouAqG9ij6UKldZI=";
    };
    phases = ["installPhase" "patchPhase"];
    installPhase = ''
      mkdir -p $out/bin
      cp $src $out/bin/bigquery-emulator
      chmod +x $out/bin/bigquery-emulator
    '';
  };

# Install our dependencies with soruces defined above.
in
  pkgs.mkShell {
    name = "projects.ki-ckstart-python";

    buildInputs = [
      google-sdk
      bigquery-emulator
      pinned.autoPatchelfHook
      pinned.direnv
      pinned.docker
      pinned.git
      pinned.pre-commit
      pinned.python312
      pinned.poetry
    ];

    nativeBuildInputs = [ pinned.autoPatchelfHook ];

    # Set the required env vars to run the app.
    NIX_LDFLAGS = if system ? "x86_64-linux" then [ "-lstdc++"] else [];
    LANG="en_UK.UTF-8";

    shellHook = ''
      PATH="${google-sdk}:${bigquery-emulator}:${pinned.poetry}:${pinned.python312}/bin:$PATH";
    '';
}
