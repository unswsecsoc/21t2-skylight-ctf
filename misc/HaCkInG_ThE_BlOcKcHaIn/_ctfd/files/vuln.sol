pragma solidity >=0.7.0 <0.8.0;

// SPDX-License-Identifier: UNLICENSED

contract Vuln
{
    uint256[] arr;
    uint256 flag = 0;

    function getFlag() view public returns (uint256)
    {
        return flag;
    }

    function setArrayLen(uint256 len) public
    {
        assembly {
            sstore(0, len)
        }
    }

    function setArrayValue(uint256 key) public
    {
        arr[key] = 1;
    }
}
