class Kaferry < Formula
  desc "Copy Kafka records and Avro archives with SQL"
  homepage "https://github.com/pagrus7/kaferry"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/pagrus7/kaferry/releases/download/v0.12.0/kaferry-v0.12.0-darwin-arm64.tar.gz"
      sha256 "ba9fb73ea7297c1b4defdc6206117ce72e57f2ac10f7435f8cb2e3f220dda689"
    end
    on_intel do
      url "https://github.com/pagrus7/kaferry/releases/download/v0.12.0/kaferry-v0.12.0-darwin-amd64.tar.gz"
      sha256 "d61de74cf850160c62ad468af30decd3731457f705cb8cdf6e02d5b67d9dcbdc"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/pagrus7/kaferry/releases/download/v0.12.0/kaferry-v0.12.0-linux-arm64.tar.gz"
      sha256 "feeb2fe5e994bbe86a93bef14fcae1fb755cc8e274a5791689c1f92ff9afc7a7"
    end
    on_intel do
      url "https://github.com/pagrus7/kaferry/releases/download/v0.12.0/kaferry-v0.12.0-linux-amd64.tar.gz"
      sha256 "815b8c1929e9115f6b3ed3ff1eef108b707dca3c78b2ec6d93622aa982c9d2bb"
    end
  end

  def install
    bin.install "kaferry"
    pkgshare.install "LICENSE", "THIRD_PARTY_NOTICES.txt"
  end

  test do
    output = shell_output("#{bin}/kaferry --version")
    assert_match "kaferry v0.12.0 (commit c7f65b8378f6bbb7b1216783269c669fcec1258a; ", output
    assert_match "MIT License", (pkgshare/"LICENSE").read
    assert_match "Go runtime and standard library", (pkgshare/"THIRD_PARTY_NOTICES.txt").read
  end
end
