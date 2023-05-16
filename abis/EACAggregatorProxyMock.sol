// SPDX-License-Identifier: None
pragma solidity 0.8.3;

contract ChainlinkAggMock {  

    uint80 roundIdCurrent;
    int256 answerCurrent;
    uint256 startedAtCurrent;
    uint256 updatedAtCurrent;
    uint80 answeredInRoundCurrent;

    uint80 roundIdPrev;
    int256 answerPrev;
    uint256 startedAtPrev;
    uint256 updatedAtPrev;
    uint80 answeredInRoundPrev;

    function latestRoundData() 
        public 
        view 
        returns (
            uint80 roundId, 
            int256 answer, 
            uint256 startedAt, 
            uint256 updatedAt, 
            uint80 answeredInRound
        ) 
    {
        return (
            roundIdCurrent, 
            answerCurrent, 
            startedAtCurrent, 
            updatedAtCurrent, 
            answeredInRoundCurrent
        );
    }

    function getRoundData(uint80 _roundId) 
        public 
        view 
        returns (
            uint80 roundId, 
            int256 answer, 
            uint256 startedAt, 
            uint256 updatedAt, 
            uint80 answeredInRound
        ) 
    {
        return (
            roundIdPrev, 
            answerPrev, 
            startedAtPrev, 
            updatedAtPrev, 
            answeredInRoundPrev
        );
    }
  
    function submitValueMock(int256 _answer) public {
        roundIdPrev = roundIdCurrent;
        answerPrev = answerCurrent;
        startedAtPrev = startedAtCurrent;
        updatedAtPrev = updatedAtCurrent;
        answeredInRoundPrev = answeredInRoundCurrent;

        roundIdCurrent++;
        answerCurrent = _answer;
        startedAtCurrent = block.timestamp;
        updatedAtCurrent = block.timestamp;
        answeredInRoundCurrent++;
    }

    function setTimestamp(uint256 _timestamp) public {
        updatedAtCurrent = _timestamp;
    }

    function setRoundId(uint80 _roundId) public {
        roundIdCurrent = _roundId;
    }

    function setAge(uint256 _ageSeconds) public {
        updatedAtCurrent = block.timestamp - _ageSeconds;
    }

    function setAnswer(int256 _answer) public {
        answerCurrent = _answer;
    }    
}


