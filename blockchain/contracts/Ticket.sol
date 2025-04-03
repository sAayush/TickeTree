// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract TicketNFT is ERC721, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    enum TicketType { MOVIE, EVENT }
    
    struct Ticket {
        uint256 id;
        address owner;
        uint256 eventId;
        uint256 showId;
        TicketType ticketType;
        uint256 price;
        bool isUsed;
        bool isRefunded;
        uint256 purchaseTime;
        string seatNumber;
    }

    mapping(uint256 => Ticket) public tickets;
    mapping(uint256 => uint256) public eventShowTicketCount; // eventId => showId => count
    mapping(uint256 => uint256) public maxTicketsPerShow; // showId => maxTickets

    event TicketPurchased(uint256 indexed ticketId, address indexed buyer, uint256 eventId, uint256 showId, TicketType ticketType);
    event TicketUsed(uint256 indexed ticketId);
    event TicketRefunded(uint256 indexed ticketId);

    constructor() ERC721("TicketTree", "TTT") {}

    function setMaxTicketsForShow(uint256 showId, uint256 maxTickets) public onlyOwner {
        maxTicketsPerShow[showId] = maxTickets;
    }

    function purchaseTicket(
        uint256 eventId,
        uint256 showId,
        TicketType ticketType,
        uint256 price,
        string memory seatNumber
    ) public payable {
        require(msg.value >= price, "Insufficient payment");
        require(eventShowTicketCount[showId] < maxTicketsPerShow[showId], "Show is sold out");
        
        _tokenIds.increment();
        uint256 newTicketId = _tokenIds.current();

        tickets[newTicketId] = Ticket({
            id: newTicketId,
            owner: msg.sender,
            eventId: eventId,
            showId: showId,
            ticketType: ticketType,
            price: price,
            isUsed: false,
            isRefunded: false,
            purchaseTime: block.timestamp,
            seatNumber: seatNumber
        });

        _mint(msg.sender, newTicketId);
        eventShowTicketCount[showId]++;
        
        emit TicketPurchased(newTicketId, msg.sender, eventId, showId, ticketType);
    }

    function verifyTicket(uint256 ticketId) public view returns (bool) {
        require(_exists(ticketId), "Ticket does not exist");
        Ticket memory ticket = tickets[ticketId];
        return ticket.owner == msg.sender && !ticket.isUsed && !ticket.isRefunded;
    }

    function useTicket(uint256 ticketId) public {
        require(_exists(ticketId), "Ticket does not exist");
        Ticket storage ticket = tickets[ticketId];
        require(ticket.owner == msg.sender, "Not the ticket owner");
        require(!ticket.isUsed, "Ticket already used");
        require(!ticket.isRefunded, "Ticket was refunded");

        ticket.isUsed = true;
        emit TicketUsed(ticketId);
    }

    function refundTicket(uint256 ticketId) public {
        require(_exists(ticketId), "Ticket does not exist");
        Ticket storage ticket = tickets[ticketId];
        require(ticket.owner == msg.sender, "Not the ticket owner");
        require(!ticket.isUsed, "Ticket already used");
        require(!ticket.isRefunded, "Ticket already refunded");
        require(block.timestamp <= ticket.purchaseTime + 24 hours, "Refund period expired");

        ticket.isRefunded = true;
        payable(msg.sender).transfer(ticket.price);
        eventShowTicketCount[ticket.showId]--;
        
        emit TicketRefunded(ticketId);
    }

    function getTicketDetails(uint256 ticketId) public view returns (
        address owner,
        uint256 eventId,
        uint256 showId,
        TicketType ticketType,
        uint256 price,
        bool isUsed,
        bool isRefunded,
        string memory seatNumber
    ) {
        require(_exists(ticketId), "Ticket does not exist");
        Ticket memory ticket = tickets[ticketId];
        return (
            ticket.owner,
            ticket.eventId,
            ticket.showId,
            ticket.ticketType,
            ticket.price,
            ticket.isUsed,
            ticket.isRefunded,
            ticket.seatNumber
        );
    }

    function withdraw() public onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}
