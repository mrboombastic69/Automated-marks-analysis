document.addEventListener('DOMContentLoaded', function() {
    // Function to fetch file history
    function fetchFileHistory(page = 1, perPage = 10, sortBy = 'created_on', order = 'asc') {
        const url = new URL('http://127.0.0.1:5000/database/history');
        url.searchParams.append('page', page);
        url.searchParams.append('per_page', perPage);
        url.searchParams.append('sort_by', sortBy);
        url.searchParams.append('order', order);

        fetch(url)
            .then(response => response.json())
            .then(data => {
                displayFiles(data.files);
                displayPagination(data.pagination);
            })
            .catch(error => console.error('Error fetching file history:', error));
    }

    // Function to display files
    function displayFiles(files) {
        const fileTable = document.getElementById('file-table-body');
        fileTable.innerHTML = ''; // Clear existing content
        
        files.forEach(file => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${file.id}</td>
                <td>${file.name}</td>
                <td>${file.created_on}</td>
                <td>${file.department}</td>
                <td><a href="${file.file_url}" download>Download</a></td>
            `;
            fileTable.appendChild(row);
        });
    }

    // Function to display pagination
    function displayPagination(pagination) {
        const paginationDiv = document.getElementById('pagination');
        paginationDiv.innerHTML = ''; // Clear existing content

        if (pagination.has_prev) {
            const prevLink = document.createElement('a');
            prevLink.href = '#';
            prevLink.textContent = 'Previous';
            prevLink.onclick = () => {
                fetchFileHistory(pagination.page - 1);
                return false; // Prevent default link behavior
            };
            paginationDiv.appendChild(prevLink);
        }

        if (pagination.has_next) {
            const nextLink = document.createElement('a');
            nextLink.href = '#';
            nextLink.textContent = 'Next';
            nextLink.onclick = () => {
                fetchFileHistory(pagination.page + 1);
                return false; // Prevent default link behavior
            };
            paginationDiv.appendChild(nextLink);
        }

        paginationDiv.innerHTML += `<p>Page ${pagination.page} of ${pagination.pages}</p>`;
    }

    // Fetch file history on page load
    fetchFileHistory();
});
