import pytest
from utils.test import create_cipher_key


def test_exact_length_master_password():
    """Tests the CipherKey class with exact length master password that requires no padding or trimming."""

    master_password = '*fg*=TY%m2Y~:dQq'
    master_key = 2466
    expected_result = 'YqdT:Q*mf2g%~=Y*'
    assert expected_result, create_cipher_key(master_password, master_key)


def test_shorter_master_password():
    """Tests the CipherKey class with shorter length master password that requires padding."""

    master_password = '3[[7W*Zj$T'
    master_key = 659
    expected_result = 'T*[3$WW7Z[[3*j[7'
    assert expected_result, create_cipher_key(master_password, master_key)


def test_longer_master_password():
    """Tests the CipherKey class with shorter length master password that requires trimming."""

    master_password = '.$4twd?iw>=q[p:d<#n!?<7!@]\';9!'
    master_key = 13392
    expected_result = '$=d.w>t4w[iq:p?d'
    assert expected_result, create_cipher_key(master_password, master_key)


def test_zero_master_key():
    """Tests that zero master key doesn't result in error."""

    master_password = 'eO!)T>6h`c}l'
    master_key = 0
    expected_result = 'ec}!6`eOO>Th)l)!'
    assert expected_result, create_cipher_key(master_password, master_key)


def test_illegal_master_password():
    """Tests that empty master password throws an error."""

    master_password = ''
    master_key = 334
    try:
        create_cipher_key(master_password, master_key)
        pytest.xfail('Expected exception as the master password was empty')
    except Exception as e:
        pass


def test_illegal_master_key():
    """Tests that negative master key throws an error."""

    master_password = 'sdal67g34'
    master_key = -642
    try:
        create_cipher_key(master_password, master_key)
        pytest.xfail('Expected exception as the master key was negative')
    except Exception as e:
        pass
