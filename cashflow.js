const express = require('express');
const app = express();
const PORT = 3000;

// Sample transaction data (you can use a real database)
let transactions = [
  { id: 1, description: "Product Sale", type: "income", amount: 100 },
  { id: 2, description: "Shipping Cost", type: "expense", amount: 10 },
  { id: 3, description: "Product Sale", type: "income", amount: 200 },
  { id: 4, description: "Refund", type: "expense", amount: 50 }
];

// Function to calculate cash flow
const calculateCashFlow = (transactions) => {
  let income = 0;
  let expense = 0;

  transactions.forEach(transaction => {
    if (transaction.type === "income") {
      income += transaction.amount;
    } else if (transaction.type === "expense") {
      expense += transaction.amount;
    }
  });

  return {
    income: income,
    expense: expense,
    netCashFlow: income - expense
  };
};

// API to get cash flow data
app.get('/cashflow', (req, res) => {
  const cashFlow = calculateCashFlow(transactions);
  res.json(cashFlow);
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
