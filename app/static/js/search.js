const searchInput = document.getElementById("searchInput");
const searchResults = document.getElementById("searchResults");

searchInput.addEventListener("input", function() {
    const keyword = searchInput.value.trim();

    if (keyword.length === 0) {
        searchResults.innerHTML = "";
        return;
    }

    // Send an AJAX request to fetch matching items
    fetchMatchingItems(keyword);
});

function fetchMatchingItems(keyword) {
    // Replace this URL with the actual endpoint to retrieve matching items from your server
    const apiUrl = `/api/search/`+keyword;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            displaySearchResults(data);
        })
        .catch(error => {
            console.error("Error fetching data: " + error);
        });
}

function displaySearchResults(matchingItems) {
    // Clear the previous results
    searchResults.innerHTML = "";

    if (matchingItems.length === 0) {
        const noResultsItem = document.createElement("li");
        noResultsItem.textContent = "No matching items found";
        searchResults.appendChild(noResultsItem);
    } else {
        matchingItems.forEach(item => {
            const listItem = document.createElement("li");
            listItem.textContent = item;
            listItem.addEventListener("click", function() {
                searchInput.value = item;
                searchResults.innerHTML = "";
            });
            searchResults.appendChild(listItem);
        });
    }
}

document.addEventListener("click", function(event) {
    if (!searchInput.contains(event.target) && !searchResults.contains(event.target)) {
        searchResults.innerHTML = "";
    }
});

searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();  // Prevent the form from submitting
            const query = searchInput.value;
            redirectToSearchResults(query);
        }
});
function redirectToSearchResults(query) {
        // Redirect to a new link based on the user's query
        window.location.href = '/search/default/' + encodeURIComponent(query);}

let count = 0;

function updateCounter() {
    const counterElement = document.getElementById('count');
    counterElement.textContent = count;
}

function incrementCounter() {
    count++;
    updateCounter();
}

function decrementCounter() {
    if (count > 0) {
        count--;
        updateCounter();
    }
}

