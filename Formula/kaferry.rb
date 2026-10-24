class Kaferry < Formula
  desc "Copy Kafka records and Avro archives with SQL"
  homepage "https://github.com/pagrus7/kaferry"
  version "0.5.0"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/pagrus7/kaferry/releases/download/v0.5.0/kaferry-v0.5.0-darwin-arm64.tar.gz"
      sha256 "1a237c4705c7ae14327d47cc4ef517c365e66cbf22ca7fbe0c0b8e047f8f4da5"
    end
    on_intel do
      url "https://github.com/pagrus7/kaferry/releases/download/v0.5.0/kaferry-v0.5.0-darwin-amd64.tar.gz"
      sha256 "b4df81949f518eaf1fa65b808cb35c46b8fee0441ba43d6931e362ef21623b46"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/pagrus7/kaferry/releases/download/v0.5.0/kaferry-v0.5.0-linux-arm64.tar.gz"
      sha256 "6105ab72f82a61a3c4a0c07c46adb57b717b4c4793b9d749abc581ad589196f8"
    end
    on_intel do
      url "https://github.com/pagrus7/kaferry/releases/download/v0.5.0/kaferry-v0.5.0-linux-amd64.tar.gz"
      sha256 "9011c8673b0d58f63616e7346767f3fd150ce713964daa1f78bb683a10a5ea04"
    end
  end

  def install
    bin.install "kaferry"
    pkgshare.install "LICENSE", "THIRD_PARTY_NOTICES.txt"
  end

  test do
    output = shell_output("#{bin}/kaferry --version")
    assert_match "kaferry v0.5.0 (commit 797cb99495bcffa7eabd5a8e1c0aa3330be66a71; ", output
    assert_match "MIT License", (pkgshare/"LICENSE").read
    assert_match "Go runtime and standard library", (pkgshare/"THIRD_PARTY_NOTICES.txt").read
  end
end
