// SPDX-License-Identifier: CC0-1.0
pragma solidity >=0.8.0;
contract NonComponentContract{
    uint256 ethPrice=1000;

    function getETHPrice()public view returns (uint256){
        return ethPrice;
    }
    function setETHPrice(uint256 _price)public{
        ethPrice=_price;
    }
}