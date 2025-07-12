document.addEventListener('DOMContentLoaded', function () {
  const allResults = JSON.parse(document.getElementById("resultsData").textContent);
  const tbody = document.querySelector("#resultsTable tbody");

  function renderTable(data) {
    tbody.innerHTML = "";
    data.forEach(item => {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td>${item.number}</td><td>${item.price}</td><td>${item.location}</td>`;
      tbody.appendChild(tr);
    });
  }

  function populateTSCOptions(data) {
    const select = document.getElementById("tscFilter");
    const locations = [...new Set(data.map(item => item.location))];
    locations.forEach(loc => {
      const option = document.createElement("option");
      option.value = loc;
      option.textContent = loc;
      select.appendChild(option);
    });
  }

  function applyFiltersAndSort() {
    const searchValue = document.getElementById("searchNumber").value.trim();
    const selectedPrice = document.getElementById("priceFilter").value;
    const selectedTSC = document.getElementById("tscFilter").value;
    const sortOrder = document.getElementById("sortPrice").value;

    let filtered = allResults.filter(item => {
      const matchesNumber = !searchValue || item.number.includes(searchValue);
      const matchesPrice = !selectedPrice || item.price === selectedPrice;
      const matchesTSC = !selectedTSC || item.location === selectedTSC;
      return matchesNumber && matchesPrice && matchesTSC;
    });

    if (sortOrder === "asc") {
      filtered.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
    } else if (sortOrder === "desc") {
      filtered.sort((a, b) => parseFloat(b.price) - parseFloat(a.price));
    }

    renderTable(filtered);
  }

  document.getElementById("applyFiltersBtn").addEventListener("click", applyFiltersAndSort);
  document.getElementById("sortPrice").addEventListener("change", applyFiltersAndSort);

  // Экспорт в Excel
  document.getElementById("exportBtn").addEventListener("click", function () {
    const rows = [["Номер", "Ціна", "Місце"]];
    document.querySelectorAll("#resultsTable tbody tr").forEach(tr => {
      const cols = tr.querySelectorAll("td");
      rows.push([cols[0].textContent, cols[1].textContent, cols[2].textContent]);
    });

    // Генерация Excel-файла
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.aoa_to_sheet(rows);
    XLSX.utils.book_append_sheet(wb, ws, "Результати");
    XLSX.writeFile(wb, "результати_пошуку.xlsx");
  });

  // Инициализация
  renderTable(allResults);
  populateTSCOptions(allResults);
});