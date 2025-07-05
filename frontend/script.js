// JavaScript sends JSON to Flask using fetch() (AJAX).
//Flask processes it and sends back JSON.
//JavaScript updates the UI with the result without refreshing the page.

// Inline Knowledge Check logic
document.getElementById('knowYes').addEventListener('click', () => {
    // Hide the question so user can see the tools
    document.querySelector('.alert-warning').style.display = 'none';
  });
  document.getElementById('knowNo').addEventListener('click', () => {
    window.location.href = 'study_guide.html';
  });
  

// Update cipher-specific input visibility
function updateCipherOptions() {
    const subCipher = document.getElementById("substitutionCipher").value;
    const transCipher = document.getElementById("transpositionCipher").value;

    // Detect which cipher is selected (substitution takes priority)
    let cipher = subCipher !== "caesar" && subCipher !== "vigenere" && subCipher !== "playfair"
        ? transCipher
        : subCipher;

    // Hide all input sections
    document.getElementById("caesarOptions").style.display = "none";
    document.getElementById("vigenereOptions").style.display = "none";
    document.getElementById("playfairOptions").style.display = "none";
    document.getElementById("railfenceOptions").style.display = "none";
    document.getElementById("columnarOptions").style.display = "none";

    // Show only the selected cipher's input
    if (cipher === "caesar") {
        document.getElementById("caesarOptions").style.display = "block";
    } else if (cipher === "vigenere") {
        document.getElementById("vigenereOptions").style.display = "block";
    } else if (cipher === "playfair") {
        document.getElementById("playfairOptions").style.display = "block";
    } else if (cipher === "railfence") {
        document.getElementById("railfenceOptions").style.display = "block";
    } else if (cipher === "columnar") {
        document.getElementById("columnarOptions").style.display = "block";
    }
}

// Ensure only one dropdown is active at a time
const subCipher = document.getElementById("substitutionCipher");
const transCipher = document.getElementById("transpositionCipher");

if (subCipher && transCipher) {
    subCipher.addEventListener("change", function () {
        document.getElementById("transpositionCipher").value = "";
        updateCipherOptions();
    });

    transCipher.addEventListener("change", function () {
        document.getElementById("substitutionCipher").value = "";
        updateCipherOptions();
    });
}

// Toggle dark mode
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
}


// This function sends the ciphertext to the backend to brute-force all 25 Caesar cipher shifts
async function bruteForceCaesar() {
    // Get input ciphertext and relevant UI elements
    let ciphertext = document.getElementById("ciphertext").value;
    let outputList = document.getElementById("outputList");
    let loadingSpinner = document.getElementById("loadingSpinner");

    // If no text entered, show warning and stop the function
    if (!ciphertext.trim()) {
        outputList.innerHTML = "<p class='text-danger'>⚠️ Enter encrypted text first before running</p>";
        return;
    }

    // Clear previous results and show loading spinner
    outputList.innerHTML = "";
    loadingSpinner.style.display = "block";

    try {
        // Send a POST request to the backend '/bruteforce' route with ciphertext as JSON
        let response = await fetch("http://127.0.0.1:5000/bruteforce", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: ciphertext })
        });

        // Parse the JSON response containing all decryption results for each shift
        let result = await response.json();
        outputList.innerHTML = "";  // Clear output again (optional but safe)

        // Loop over each Caesar shift (0–25) and display its result as a Bootstrap card
        Object.keys(result.output).forEach(shift => {
            let card = document.createElement("div");
            card.classList.add("card", "mb-2", "p-2");

            let cardBody = document.createElement("div");
            cardBody.classList.add("card-body");

            // Title shows which Caesar shift this result corresponds to
            let title = document.createElement("h6");
            title.classList.add("card-title", "fw-bold");
            title.textContent = `Shift ${shift}:`;

            // Text shows the decrypted message for that shift
            let text = document.createElement("p");
            text.classList.add("card-text");
            text.textContent = result.output[shift];

            // Build the card and add to the result container
            cardBody.appendChild(title);
            cardBody.appendChild(text);
            card.appendChild(cardBody);
            outputList.appendChild(card);
        });

    } catch (error) {
        // If request fails, show error message
        outputList.innerHTML = "<p class='text-danger'>❌ Error: Not able to process request!.</p>";
    } finally {
        // Hide the loading spinner once done (success or error)
        loadingSpinner.style.display = "none";
    }
}


// Update character count
function updateCharCount() {
    let count = document.getElementById("ciphertext").value.length;
    document.getElementById("charCount").textContent = count + " characters"; 
}

// Process text (encrypt/decrypt)
async function processText(action) {
    const text = document.getElementById("textInput").value;
    const subCipher = document.getElementById("substitutionCipher").value;
    const transCipher = document.getElementById("transpositionCipher").value;

    // Determine selected cipher
    let cipherType = subCipher !== "caesar" && subCipher !== "vigenere" && subCipher !== "playfair"
        ? transCipher
        : subCipher;

    const data = { text, action, cipher: cipherType };

    // Add cipher-specific parameters
    if (cipherType === "caesar") {
        data.shift = parseInt(document.getElementById("shiftValue").value);
    } else if (cipherType === "vigenere") {
        data.key = document.getElementById("vigenereKey").value;
    } else if (cipherType === "playfair") {
        data.key = document.getElementById("playfairKey").value;
    } else if (cipherType === "railfence") {
        data.rails = parseInt(document.getElementById("railfenceRails").value);
    } else if (cipherType === "columnar") {
        data.key = document.getElementById("columnarKey").value.trim();
    }

    document.getElementById("loadingSpinner").style.display = "block";
    document.getElementById("outputText").textContent = "";
    document.getElementById("railFenceGrid").style.display = "none";
    document.getElementById("gridButtonContainer").style.display = "none";

    try {
        const response = await fetch("http://127.0.0.1:5000/process", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        // grid
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        document.getElementById("outputText").textContent = result.output;

        // Show grid button only for Rail Fence
        const cipherType = data.cipher;
        const gridContainer = document.getElementById("railFenceGrid");
        const gridButton = document.getElementById("gridButtonContainer");

        if (cipherType === "railfence") {
            gridButton.style.display = "block";
            gridContainer.style.display = "none";
        } else {
            gridButton.style.display = "none";
            gridContainer.style.display = "none";
        }
        
        
    } catch (error) {
        document.getElementById("outputText").textContent = "Error: Unable to process request.";
        document.getElementById("gridButtonContainer").style.display = "none";
        document.getElementById("railFenceGrid").style.display = "none";
    } finally {
        document.getElementById("loadingSpinner").style.display = "none";
    }
}

// Toggle sidebar navigation
document.getElementById("navToggle").onclick = function() {
    let sidebar = document.getElementById("mySidebar");
    if (sidebar.style.left === "-250px") {
        sidebar.style.left = "0px";
    } else {
        sidebar.style.left = "-250px";
    }
}

// Close sidebar navigation
function closeNav() {
    let sidebar = document.getElementById("mySidebar");
    sidebar.style.left = "-250px";
}

//Function to display railfence grids
function showRailFenceGrid() {
    const text = document.getElementById("textInput").value;
    const rails = parseInt(document.getElementById("railfenceRails").value);
    const action = document.querySelector('button[onclick*="encrypt"]').disabled 
        ? 'decrypt' 
        : 'encrypt';
    
    if (!text) {
        alert("Please enter text first!");
        return;
    }
    
    document.getElementById("gridVisualization").innerHTML = generateRailFenceGrid(text, rails, action);
    document.getElementById("railFenceGrid").style.display = "block";
    
    // Scroll to the grid
    document.getElementById("railFenceGrid").scrollIntoView({ 
        behavior: 'smooth' 
    });
}


// function to generate railfence grid
function generateRailFenceGrid(text, rails) {
    const grid = Array(rails).fill().map(() => Array(text.length).fill(null));
    let currentRail = 0;
    let direction = 1;

    // Mark character positions
    for (let i = 0; i < text.length; i++) {
        grid[currentRail][i] = text[i];
        if (currentRail === 0) direction = 1;
        else if (currentRail === rails - 1) direction = -1;
        currentRail += direction;
    }

    // Generate HTML
    let html = '<div class="rail-fence-grid"><table>';
    for (let r = 0; r < rails; r++) {
        html += '<tr>';
        for (let c = 0; c < text.length; c++) {
            const hasChar = grid[r][c] !== null;
            const cellClass = hasChar ? 'character-cell' : '';
            const content = hasChar ? grid[r][c] : '&nbsp;';
            html += `<td class="${cellClass}">${content}</td>`;
        }
        html += '</tr>';
    }
    html += '</table></div>';
    
    return html;
}



// Frequency analysis script
async function performFrequencyAnalysis() {
    let text = document.getElementById("analysisText").value;
    let frequencyTable = document.getElementById("frequencyTable");
    let comparisonTable = document.getElementById("comparisonTable");
    let loadingSpinner = document.getElementById("loadingSpinner");

    if (!text.trim()) {
        frequencyTable.innerHTML = "<tr><td colspan='2' class='text-danger'>⚠️ Please enter text first.</td></tr>";
        comparisonTable.innerHTML = "<tr><td colspan='3' class='text-danger'>⚠️ No comparison available.</td></tr>";
        return;
    }

    frequencyTable.innerHTML = "";
    comparisonTable.innerHTML = "";
    loadingSpinner.style.display = "block";

    try {
        let response = await fetch("http://127.0.0.1:5000/frequency-analysis", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        });

        let result = await response.json();
        frequencyTable.innerHTML = "";  
        comparisonTable.innerHTML = "";

        let labels = [];
        let counts = [];

        // Standard English letter frequencies (from backend)
        const englishFrequencies = result.english_frequencies;

        Object.keys(result.frequencies).forEach(letter => {
            let yourFrequency = result.frequencies[letter];
            let englishFreq = englishFrequencies[letter] || 0;

            // Fill Letter Frequency Table
            let row = document.createElement("tr");
            row.innerHTML = `<td>${letter}</td><td>${yourFrequency}%</td>`;
            frequencyTable.appendChild(row);

            // Fill Frequency Comparison Table
            let compRow = document.createElement("tr");
            compRow.innerHTML = `<td>${letter}</td><td>${yourFrequency}%</td><td>${englishFreq}%</td>`;
            comparisonTable.appendChild(compRow);

            labels.push(letter);
            counts.push(yourFrequency);
        });

        updateFrequencyChart(labels, counts, englishFrequencies);

    } catch (error) {
        frequencyTable.innerHTML = "<tr><td colspan='2' class='text-danger'>❌ Error: Unable to process request.</td></tr>";
        comparisonTable.innerHTML = "<tr><td colspan='3' class='text-danger'>❌ Error fetching data.</td></tr>";
    } finally {
        loadingSpinner.style.display = "none";
    }
}

// Frequency analysis chart
function updateFrequencyChart(labels, counts, englishFrequencies) {
    let ctx = document.getElementById("frequencyChart").getContext("2d");

    if (window.freqChart) {
        window.freqChart.destroy();
    }

    let englishCounts = labels.map(letter => englishFrequencies[letter] || 0);

    window.freqChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Your Text (%)",
                    data: counts,
                    backgroundColor: "rgba(54, 162, 235, 0.5)",
                    borderColor: "rgba(54, 162, 235, 1)",
                    borderWidth: 1
                },
                {
                    label: "English (%)",
                    data: englishCounts,
                    backgroundColor: "rgba(255, 99, 132, 0.5)",
                    borderColor: "rgba(255, 99, 132, 1)",
                    borderWidth: 1
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// to download frequency analysis chart as png
function downloadChartImage() {
    const canvas = document.getElementById("frequencyChart");
    const link = document.createElement("a");
    link.download = "frequency_analysis_chart.png";
    link.href = canvas.toDataURL("image/png", 1.0);
    link.click();
}


// Analyze frequency of ciphertext (for crack_cipher.html)
async function analyzeCiphertext() {
    const text = document.getElementById("cipherInput").value;
    const frequencyTable = document.getElementById("frequencyTable");
    const ctx = document.getElementById("frequencyChart").getContext("2d");
  
    if (!text.trim()) {
      frequencyTable.innerHTML = "<tr><td colspan='3' class='text-danger'>⚠️ Please enter ciphertext.</td></tr>";
      return;
    }
  
    try {
      const res = await fetch("http://127.0.0.1:5000/manual-frequency", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ciphertext: text })
    });
  
      const result = await res.json();
      if (result.error) throw new Error(result.error);
  
      frequencyTable.innerHTML = "";
      const labels = [];
      const counts = [];
  
      result.frequencies.forEach(item => {
        frequencyTable.innerHTML += `<tr><td>${item.letter}</td><td>${item.count}</td><td>${item.percent}%</td></tr>`;
        labels.push(item.letter);
        counts.push(item.percent);
    });
  
      if (window.freqChart) window.freqChart.destroy();
      window.freqChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [{
            label: "Letter Frequency (%)",
            data: counts,
            backgroundColor: "rgba(54, 162, 235, 0.5)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: { beginAtZero: true }
          }
        }
    });
  
      //  Update the mapping table and preview when analysis is done
      updateSubstitutionTable();
      updateDecryptionPreview();
  
    } catch (err) {
      console.error("Frequency error:", err);
      frequencyTable.innerHTML = "<tr><td colspan='3' class='text-danger'>❌ Error analyzing frequencies.</td></tr>";
    }
}
  
// Substitution mapping UI generation
function updateSubstitutionTable() {
    const text = document.getElementById("cipherInput").value.toUpperCase();
    const uniqueLetters = [...new Set(text.replace(/[^A-Z]/gi, ''))].sort();
    const table = document.getElementById("substitutionTable");
    table.innerHTML = "";
  
    uniqueLetters.forEach(letter => {
      table.innerHTML += `<tr><td>${letter}</td><td><input type='text' maxlength='1' class='form-control form-control-sm guess-input' data-letter='${letter}'></td></tr>`;
    });
  
    document.querySelectorAll(".guess-input").forEach(input => {
      input.addEventListener("input", updateDecryptionPreview);
    });
}
  
// Apply user mapping and get decrypted preview
function updateDecryptionPreview() {
    const text = document.getElementById("cipherInput").value;
    const mapInputs = document.querySelectorAll(".guess-input");
    const mapping = {};

    mapInputs.forEach(input => {
        const letter = input.dataset.letter;
        const guess = input.value.toUpperCase();
        mapping[letter] = guess || null;
    });

    fetch("http://127.0.0.1:5000/apply-mapping", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ciphertext: text, mapping: mapping })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("cipherDisplay").textContent = text;

        let highlighted = '';
        for (let i = 0; i < text.length; i++) {
            const char = text[i];
            const upper = char.toUpperCase();
            if (/[A-Z]/.test(upper) && mapping[upper]) {
                const sub = mapping[upper];
                const repl = char === upper ? sub : sub.toLowerCase();
                highlighted += `<span class="text-success fw-bold">${repl}</span>`;
            } else {
                highlighted += `<span class="text-muted">${char}</span>`;
            }
        }

        document.getElementById("plaintextPreview").innerHTML = highlighted;
    })
    .catch(() => {
        document.getElementById("plaintextPreview").textContent = "❌ Error previewing decryption.";
    });
}

  // Reset user mappings
  function resetMappings() {
    document.querySelectorAll(".guess-input").forEach(input => input.value = "");
    updateDecryptionPreview();
}
  
  // Load example ciphertext
  function loadExample() {
    document.getElementById("cipherInput").value = "ORANGE IS BOTH, A COLOR AND A FRUIT!";
    updateSubstitutionTable();
    analyzeCiphertext();
    updateDecryptionPreview();
}

// Detect cipher
async function detectCipherType() {
    const text = document.getElementById("cipherInput").value.trim();
    const hint = document.getElementById("cipherHint");
    
    if (!text) {
        hint.innerHTML = '<span class="badge bg-warning">⚠️ Enter ciphertext first</span>';
        return;
    }

    hint.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Analyzing...';
    
    try {
        const response = await fetch("http://127.0.0.1:5000/detect-cipher-type", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({ ciphertext: text })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.suggestion || "Detection failed");
        }

        const result = await response.json();
        
        if (result.status === "error") {
            throw new Error(result.suggestion);
        }

        // Success case
        const isSubstitution = result.suggestion.includes("Substitution");
        hint.innerHTML = `
            <span class="badge ${isSubstitution ? 'bg-primary' : 'bg-warning text-dark'}">
                🔍 ${result.suggestion}
            </span>
        `;
        
    } catch (error) {
        hint.innerHTML = `
            <span class="badge bg-danger">
                ❌ ${error.message || "Detection failed"}
            </span>
        `;
        console.error("Detection error:", error);
    }
}

// dictionary help
function dictionaryHelp() {
    const inputBox = document.getElementById('dictionaryInputBox');
    const suggestionArea = document.getElementById('suggestionsBox');
    inputBox.style.display = inputBox.style.display === 'none' ? 'block' : 'none';
    suggestionArea.innerHTML = ""; // clear previous suggestions
}

// Listen for user input and fetch suggestions automatically 
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("patternInput");
    if (input) {
        input.addEventListener("input", async () => {
            const pattern = input.value.trim();
            const suggestionBox = document.getElementById("suggestionsBox");
            suggestionBox.innerHTML = "";

            if (!pattern || pattern.length < 3) return;

            try {
                const response = await fetch("http://127.0.0.1:5000/dictionary-suggest", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ pattern })
                });

                const result = await response.json();
                if (result.error) {
                    suggestionBox.innerHTML = `<p class="text-danger">${result.error}</p>`;
                    return;
                }

                if (result.matches.length === 0) {
                    suggestionBox.innerHTML = `<p class="text-muted">No matches found.</p>`;
                    return;
                }

                result.matches.forEach(word => {
                    const badge = document.createElement("span");
                    badge.className = "badge bg-info text-dark m-1";
                    badge.style.cursor = "pointer";
                    badge.textContent = word;
                    suggestionBox.appendChild(badge);
                });
            } catch (err) {
                console.error("Error fetching dictionary suggestions:", err);
                suggestionBox.innerHTML = `<p class="text-danger">❌ Error fetching suggestions.</p>`;
            }
        });
    }
});

// fetch matches
async function fetchDictionaryMatches() {
    const pattern = document.getElementById("patternInput").value.trim();
    const suggestionBox = document.getElementById("suggestionsBox");
    suggestionBox.innerHTML = "";

    if (!pattern || pattern.length < 2) {
        suggestionBox.innerHTML = `<p class="text-danger">Please enter a partial word pattern.</p>`;
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/dictionary-suggest", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ pattern })
        });

        const result = await response.json();
        if (result.error) {
            suggestionBox.innerHTML = `<p class="text-danger">${result.error}</p>`;
            return;
        }

        if (result.matches.length === 0) {
            suggestionBox.innerHTML = `<p class="text-muted">No matches found.</p>`;
            return;
        }

        result.matches.forEach(word => {
            const badge = document.createElement("span");
            badge.className = "badge bg-info text-dark m-1";
            badge.textContent = word;
            suggestionBox.appendChild(badge);
        });
    } catch (err) {
        console.error("Error fetching dictionary suggestions:", err);
        suggestionBox.innerHTML = `<p class="text-danger">❌ Error fetching suggestions.</p>`;
    }
}
 
