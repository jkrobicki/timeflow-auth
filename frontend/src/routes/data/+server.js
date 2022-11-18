
export const baseUrl = "http://localhost:8003"

async function getItems() {
    const response = await fetch(`${baseUrl}/items/`, {
        method: 'GET',
        headers: { 'accept': 'application/json', 'Authorization': 'Bearer' }
    });
    let items = await response.json()
    return items
};
export { getItems }

