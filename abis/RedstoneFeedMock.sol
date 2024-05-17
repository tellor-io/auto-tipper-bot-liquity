// SPDX-License-Identifier: None
pragma solidity 0.8.3;

contract RedstoneMock {  

    uint256 public roundIdCurrent;

    struct RoundData {
        uint256 price;
        uint128 dataTimestamp;
        uint128 blockTimestamp;
    }

    mapping(uint256 => mapping(bytes32 => RoundData)) public roundData;
  
    function submitValueMock(bytes32 _dataId, uint256 _answer) public {
        roundIdCurrent++;

        RoundData storage rData = roundData[roundIdCurrent][_dataId];
        rData.price = _answer;
        rData.dataTimestamp = uint128(block.timestamp);
        rData.blockTimestamp = uint128(block.timestamp);
    }

    // redstone ******

   /**
   * @notice Returns latest successful round number
   * @return latestRoundId
   */
  function getLatestRoundId() public view returns (uint256 latestRoundId) {
    return roundIdCurrent;
  }

  /**
   * @notice Returns details for the given round and data feed
   * @param dataFeedId Requested data feed
   * @param roundId Requested round identifier
   * @return dataFeedValue
   * @return roundDataTimestamp
   * @return roundBlockTimestamp
   */
  function getRoundDataFromAdapter(
    bytes32 dataFeedId, 
    uint256 roundId) public view returns (
        uint256 dataFeedValue, 
        uint128 roundDataTimestamp, 
        uint128 roundBlockTimestamp
   ) {
    require(roundId > 0, "RoundId must be greater than 0");
    require(roundId <= getLatestRoundId(), "Invalid round id");

    RoundData memory dataFeedData = roundData[roundId][dataFeedId];
    return (dataFeedData.price, dataFeedData.dataTimestamp, dataFeedData.blockTimestamp);
  }


}


