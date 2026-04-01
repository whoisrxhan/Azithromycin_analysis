document.addEventListener("DOMContentLoaded", () => {
    fetchData();
});

async function fetchData() {
    const loadingElem = document.getElementById('loading');
    const resultsElem = document.getElementById('results');
    const errorElem = document.getElementById('error-message');

    try {
        const response = await fetch('/analyze');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }

        renderData(data);
        
        // Hide loader, show results
        loadingElem.classList.add('hidden');
        resultsElem.classList.remove('hidden');

    } catch (error) {
        console.error("Error fetching data:", error);
        loadingElem.classList.add('hidden');
        errorElem.textContent = `Error: ${error.message}. Ensure the Python backend is running correctly.`;
        errorElem.classList.remove('hidden');
    }
}

function renderData(data) {
    document.getElementById('molecule-name').textContent = data.molecule;
    document.getElementById('total-count').textContent = data.total_chiral_centers;

    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';

    if (data.centers && data.centers.length > 0) {
        data.centers.forEach((center) => {
            const tr = document.createElement('tr');
            
            // Atom Index
            const tdIndex = document.createElement('td');
            tdIndex.textContent = center.atom_index;
            // Element
            const tdElement = document.createElement('td');
            tdElement.textContent = center.element;
            // Configuration
            const tdConfig = document.createElement('td');
            
            // Badge style for R/S configs
            const badge = document.createElement('span');
            badge.textContent = center.configuration;
            badge.style.fontWeight = '600';
            if (center.configuration === 'R') {
                badge.style.color = '#047857'; // Green
                badge.style.backgroundColor = '#d1fae5';
                badge.style.padding = '0.25rem 0.5rem';
                badge.style.borderRadius = '9999px';
            } else if (center.configuration === 'S') {
                badge.style.color = '#1d4ed8'; // Blue
                badge.style.backgroundColor = '#dbeafe';
                badge.style.padding = '0.25rem 0.5rem';
                badge.style.borderRadius = '9999px';
            } else {
                badge.style.color = '#64748b'; // Gray for unassigned/others
            }

            tdConfig.appendChild(badge);

            tr.appendChild(tdIndex);
            tr.appendChild(tdElement);
            tr.appendChild(tdConfig);

            tbody.appendChild(tr);
        });
    } else {
        const tr = document.createElement('tr');
        const td = document.createElement('td');
        td.colSpan = 3;
        td.textContent = "No chiral centers found.";
        td.style.textAlign = 'center';
        td.style.color = 'var(--text-muted)';
        tr.appendChild(td);
        tbody.appendChild(tr);
    }
}
