fetch(
  "https://google-books.p.rapidapi.com/volumes?key=AIzaSyAOsteuaW5ifVvA_RkLXh0mYs6GLAD6ykc",
  {
    method: "GET",
    headers: {
      "x-rapidapi-key": "643dea22c1msh2196402f710b469p1df2fejsn33c91fd47995",
      "x-rapidapi-host": "google-books.p.rapidapi.com",
    },
  }
)
  .then((res) => res.json())
  .then((response) => {
    books = response.items;
    books.forEach((book) => {
      let container = document.querySelector(".books_container");
      container.innerHTML += `<div class="card">
      <img src="${book.volumeInfo.imageLinks["thumbnail"]}">
      <h5>${book.volumeInfo["title"]}</h5>

      <h4> by ${book.volumeInfo["authors"]}</h4>

      <a href="{{url_for('templates', filename='carts.html')}}"><button class="btn" onclick="getBooks()">Add to cart</button></a>
      </div>
    `;
    });
  });


function toggleNavbar() {
  document.getElementsByClassName("navbar-links")[0].classList.toggle("active");
}


function getBooks() {
  fetch(
    "https://google-books.p.rapidapi.com/volumes?key=AIzaSyAOsteuaW5ifVvA_RkLXh0mYs6GLAD6ykc",
    {
      method: "GET",
      headers: {
        "x-rapidapi-key": "643dea22c1msh2196402f710b469p1df2fejsn33c91fd47995",
        "x-rapidapi-host": "google-books.p.rapidapi.com",
      },
    }
  )
    .then((response) => response.json())
    .then((data) => {
      let card = document.querySelector(".book_cart");
      card.innerHTML = `<div class="carts_card">
      <div class="book_img">
        <img src="${book.volumeInfo.imageLinks["thumbnail"]}/>
      </div>
      <div class="cart_details">
        <p>${book.volumeInfo["title"]}</p>
        <p>${book.volumeInfo["authors"]}</p>
        <p>${book.volumeInfo["pageCount"] * 7}</p>
      </div>
      <div class="cart_btns">
        <button>DELETE</button>
      </div>
    </div>`;
    });
}

function filterBooks(category) {
  let books = document.getElementsByClassName("card");
  if (category == "All") {
    for (book of books) {
      card.style.display = "block";
    }
    return;
  }
  for (book of books) {
    card.style.display = "none";
  }

  let selectedCards = document.querySelectorAll(`[techStack='${category}']`);

  for (book of selectedCards) {
    book.style.display = "block";
  }
}

