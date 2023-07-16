let chartBar = undefined;

const renderChart = (data) => {
  if (chartBar !== undefined) {
    chartBar.destroy();
  }

  const labelsBarChart = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate'];
  const dataBarChart = {
    labels: labelsBarChart,
    datasets: [
      {
        label: data.comment,
        backgroundColor: "hsl(252, 82.9%, 67.8%)",
        borderColor: "hsl(252, 82.9%, 67.8%)",
        data: labelsBarChart.map(label => data.result[label] * 100)
      },
    ]
  };

  const configBarChart = {
    type: "bar",
    data: dataBarChart,
    options: {
      scales: {
        y: {
          min: 0,
          max: 100,
        }
      }
    }
  };

  chartBar = new Chart(
    document.getElementById("chartBar"),
    configBarChart
  );
}

const detectHate = async () => {
  const text = document.getElementById("text").value;
  if (text.length > 0) {
    fetch("/", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify([text])
    }).then(response => {
      return response.json()
    }).then((data) => {
      renderChart(data[0]);
      document.getElementById('hate-text').innerHTML = `Hate Chart: ${data[0].comment}`;
      document.getElementById('chart').style.display = 'block';
      document.getElementById('hate-text').scrollIntoView();
      console.log(data);
    })
  }
}
