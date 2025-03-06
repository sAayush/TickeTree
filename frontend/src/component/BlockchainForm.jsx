import React, { useState } from "react";
import axios from "axios";

const BlockchainForm = () => {
  const [sender, setSender] = useState("");
  const [recipient, setRecipient] = useState("");
  const [amount, setAmount] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/blockchain/transaction/",
        {
          sender,
          recipient,
          amount,
        }
      );
      console.log(response.data);
    } catch (error) {
      console.error("Error creating transaction:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Sender"
        value={sender}
        onChange={(e) => setSender(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Recipient"
        value={recipient}
        onChange={(e) => setRecipient(e.target.value)}
        required
      />
      <input
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        required
      />
      <button type="submit">Send Transaction</button>
    </form>
  );
};

export default BlockchainForm;
