"""Unit tests for cryptographic hashing, comparison, and format identification."""

import hashlib
from pathlib import Path

from haxmed_cryptolab.engines.hashes.comparator import HashComparator
from haxmed_cryptolab.engines.hashes.hasher import HashEngine
from haxmed_cryptolab.engines.hashes.identifier import HashIdentifier


class TestHashEngine:
    def test_known_test_vectors(self):
        # Empty string vectors
        assert (
            HashEngine.hash_text("", "SHA-256")
            == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        )
        assert HashEngine.hash_text("", "MD5") == "d41d8cd98f00b204e9800998ecf8427e"
        assert HashEngine.hash_text("", "SHA-1") == "da39a3ee5e6b4b0d3255bfef95601890afd80709"

        # "haxmed" vector
        expected_sha256 = hashlib.sha256(b"haxmed").hexdigest()
        assert HashEngine.hash_text("haxmed", "SHA-256") == expected_sha256

        expected_sha512 = hashlib.sha512(b"haxmed").hexdigest()
        assert HashEngine.hash_text("haxmed", "SHA-512") == expected_sha512

        expected_sha3_256 = hashlib.sha3_256(b"haxmed").hexdigest()
        assert HashEngine.hash_text("haxmed", "SHA3-256") == expected_sha3_256

    def test_file_hashing_chunked(self, tmp_path: Path):
        test_file = tmp_path / "sample.bin"
        # Write 256 KB of deterministic data
        data = b"HAXMED_CRYPTO_CHUNK_TEST" * 10240
        test_file.write_bytes(data)

        expected_digest = hashlib.sha256(data).hexdigest()
        computed = HashEngine.hash_file(str(test_file), "SHA-256", chunk_size_bytes=4096)
        assert computed == expected_digest


class TestHashComparator:
    def test_compare_matching_digests(self):
        h1 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        h2 = "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"
        res = HashComparator.compare(h1, h2)
        assert res.is_match is True
        assert res.status_label == "MATCH"

    def test_compare_differing_digests(self):
        h1 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        h2 = "955a153205aa3e35a396263ad2ad16a3bb02ebc83626e254e0a4f5fc5120668b"
        res = HashComparator.compare(h1, h2)
        assert res.is_match is False
        assert res.status_label == "NO MATCH"

    def test_compare_invalid_input(self):
        res = HashComparator.compare("not-a-hex-digest", "12345")
        assert res.is_match is False
        assert res.status_label == "INVALID INPUT"


class TestHashIdentifier:
    def test_identify_bcrypt(self):
        b_hash = "$2b$12$e8POdGlHFqcuhG7UmUqEuOG/9k/D8sC0z.6K29qN0Pj.j7B4iT/y2"
        candidates = HashIdentifier.identify(b_hash)
        assert len(candidates) > 0
        assert candidates[0].algorithm == "Bcrypt"

    def test_identify_argon2(self):
        a_hash = "$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$RdescudvJCsgqlfreSAeYQ"
        candidates = HashIdentifier.identify(a_hash)
        assert len(candidates) > 0
        assert "Argon2" in candidates[0].algorithm

    def test_identify_sha256(self):
        h256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        candidates = HashIdentifier.identify(h256)
        algos = [c.algorithm for c in candidates]
        assert "SHA-256" in algos
