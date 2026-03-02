function addToCart(productId) {
  fetch("/marketplace/cart/add/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCSRFToken(),
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `product_id=${productId}`,
  })
  .then(res => res.json())
  .then(() => {
    alert("Added to cart");
  });
}

function removeFromCart(productId) {
  fetch("/marketplace/cart/remove/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCSRFToken(),
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `product_id=${productId}`,
  })
  .then(() => location.reload());
}

function getCSRFToken() {
  return document.querySelector("[name=csrfmiddlewaretoken]").value;
}
