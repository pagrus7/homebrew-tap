class Kaferry < Formula
  desc "Copy Kafka records and Avro archives with SQL"
  homepage "https://github.com/pagrus7/kaferry"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/pagrus7/kaferry/releases/download/v0.6.0/kaferry-v0.6.0-darwin-arm64.tar.gz"
      sha256 "1d1b34c9138577eed67b494715545e37bdca3a99678ce23ae5375a2a65c3b293"
    end
    on_intel do
      url "https://github.com/pagrus7/kaferry/releases/download/v0.6.0/kaferry-v0.6.0-darwin-amd64.tar.gz"
      sha256 "72d9cc375fe5dcbd1a83ee50444b19ebcbcae2d4c912f5d715f1c7769b5c8385"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/pagrus7/kaferry/releases/download/v0.6.0/kaferry-v0.6.0-linux-arm64.tar.gz"
      sha256 "e79718f78eb5619e51a4505e3a87ddc37c38dd7049292bfe4b6037cbe5102bf2"
    end
    on_intel do
      url "https://github.com/pagrus7/kaferry/releases/download/v0.6.0/kaferry-v0.6.0-linux-amd64.tar.gz"
      sha256 "d1ce67ce82f610b479b0458cc7f76b4a6cdb6094f60382d58edcc484ef12670f"
    end
  end

  def install
    bin.install "kaferry"
    pkgshare.install "LICENSE", "THIRD_PARTY_NOTICES.txt"
  end

  test do
    output = shell_output("#{bin}/kaferry --version")
    assert_match "kaferry v0.6.0 (commit d7d485b96a52b711cb10d76dca09aa9b155dec5e; ", output
    assert_match "MIT License", (pkgshare/"LICENSE").read
    assert_match "Go runtime and standard library", (pkgshare/"THIRD_PARTY_NOTICES.txt").read
  end
end
