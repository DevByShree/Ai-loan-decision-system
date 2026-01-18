document.getElementById("loanForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const data = {
    Gender: document.getElementById("Gender").value,
    Married: document.getElementById("Married").value,
    Dependents: document.getElementById("Dependents").value,
    Education: document.getElementById("Education").value,
    Self_Employed: document.getElementById("Self_Employed").value,
    ApplicantIncome: Number(document.getElementById("ApplicantIncome").value),
    CoapplicantIncome: Number(document.getElementById("CoapplicantIncome").value),
    LoanAmount: Number(document.getElementById("LoanAmount").value),
    Loan_Amount_Term: Number(document.getElementById("Loan_Amount_Term").value),
    Credit_History: Number(document.getElementById("Credit_History").value),
    Property_Area: document.getElementById("Property_Area").value
  };

  const response = await fetch(
    "https://ai-loan-decision-system-4.onrender.com/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = await response.json();

  document.getElementById("decision").innerText =
    "Decision: " + result.decision;

  document.getElementById("confidence").innerText =
    `YES Probability: ${result.yes_probability}`;

  const reasonsList = document.getElementById("reasons");
  reasonsList.innerHTML = "";

  result.explanation.forEach(reason => {
    const li = document.createElement("li");
    li.innerText = reason;
    reasonsList.appendChild(li);
  });
});
document.getElementById("loanForm").reset();

