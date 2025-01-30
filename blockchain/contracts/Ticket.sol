// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TicketNFT {
    struct Ticket {
        uint256 id;
        address owner;
        uint256 eventId;
        bool isUsed;
    }

    mapping(uint256 => Ticket) public tickets;
    uint256 public nextTicketId;

    function buyTicket(uint256 eventId) public {
        tickets[nextTicketId] = Ticket(nextTicketId, msg.sender, eventId, false);
        nextTicketId++;
    }

    function verifyTicket(uint256 ticketId) public view returns (bool) {
        return tickets[ticketId].owner == msg.sender && !tickets[ticketId].isUsed;
    }
}
