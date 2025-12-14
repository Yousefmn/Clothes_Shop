
document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const username = document.getElementById("username").value.trim();
            const password = document.getElementById("password").value.trim();
            const msg = document.getElementById("loginMsg");

            msg.textContent = "Checking...";

            try {
                const response = await fetch("http://192.168.1.30:5000/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();

                if (response.ok) {
                    msg.style.color = "green";
                    msg.textContent = "Login successful!";

                    setTimeout(() => {
                        window.location.href = "index.html";
                    }, 800);
                } else {
                    msg.style.color = "red";
                    msg.textContent = data.message || "Invalid username or password.";
                }

            } catch (error) {
                console.error("Login error:", error);
                msg.style.color = "red";
                msg.textContent = "Server not responding.";
            }
        });
    }
});



async function loadProducts() {
    const container = document.querySelector(".grid-container");
    if (!container) return; 
    try {
        const response = await fetch("http://192.168.1.30:5000/products");
        const products = await response.json();

        container.innerHTML = ""; 

        products.forEach(product => {
            const card = document.createElement("div");
            card.classList.add("product-card");

            card.innerHTML = `
                <img src="img/default.jpeg" alt="${product.ProductName}">
                <div class="product-info">
                    <p>$${product.Price}</p>
                    <button class="add-btn" data-id="${product.ProductID}">Add</button>
                </div>
                <h3>${product.ProductName}</h3>
            `;

            container.appendChild(card);
        });

    } catch (error) {
        console.error("Error fetching products:", error);
        alert("Can't load products from backend.");
    }
}



document.addEventListener("click", async (e) => {
    if (e.target.classList.contains("add-btn")) {
        const productID = e.target.getAttribute("data-id");
        const price = e.target.getAttribute("data-price") || 0;  

        const orderData = {
            CustomerID: 1,
            ProductID: Number(productID),
            Quantity: 1,
            Price: Number(price)
        };

        try {
            const response = await fetch("http://192.168.1.30:5000/orders", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(orderData)
            });

            const data = await response.json();

            if (response.ok) {
                alert(`Order Added! ID = ${data.OrderID}`);
            } else {
                alert("Failed: " + data.message);
            }

        } catch (err) {
            console.error(err);
            alert("Server Offline");
        }
    }
});




document.addEventListener("DOMContentLoaded", loadProducts);
