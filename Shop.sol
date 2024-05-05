// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.2 <0.9.0;

contract Shop {
    address private owner;

    struct PriceProduct {
        uint256 price;
        string product;
    }

    PriceProduct[] public priceList;
    //PriceProduct priceProduct;
    uint256 status = 0;

    constructor() {
        owner = msg.sender;
        priceList.push(PriceProduct({price: 1, product: "bread"}));
        priceList.push(PriceProduct({price: 2, product: "tomato"}));
        priceList.push(PriceProduct({price: 3, product: "soap"}));
    }

    function getPriceList() public view returns (PriceProduct[] memory) {
        return priceList;
    }

    function buy(uint256 id) public payable returns (string memory) {
        require(id < priceList.length, "No id!");
        PriceProduct memory priceProduct2 = priceList[id];
        require(msg.value >= priceProduct2.price, "No money!");
        status = 1;
        return priceProduct2.product;
    }

    function received() public {
        require(status == 1, "Fail");
        status = 0;
    }
}
