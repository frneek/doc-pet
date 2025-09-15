document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");
  const booksContainer = document.getElementById("books");

  // === ЛОГИН ===
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;

      try {
        const res = await fetch("/api/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
          credentials: "include"
        });

        if (!res.ok) throw new Error("Ошибка авторизации");
        const data = await res.json();
        console.log("Успешный вход:", data);

        window.location.href = "/library.html";
      } catch (err) {
        alert(err.message);
      }
    });
  }

  // === РЕГИСТРАЦИЯ ===
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const username = document.getElementById("reg-username").value;
      const password = document.getElementById("reg-password").value;

      try {
        const res = await fetch("/api/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
          credentials: "include"
        });

        if (!res.ok) {
          const errData = await res.json();
          throw new Error(errData.error || "Ошибка регистрации");
        }
        alert("Регистрация успешна! Теперь войдите.");
        window.location.href = "/index.html";
      } catch (err) {
        alert(err.message);
      }
    });
  }

  // === ЗАГРУЗКА БИБЛИОТЕКИ ===
  if (booksContainer) {
    fetch("/api/library/books", {
      method: "GET",
      credentials: "include"
    })
      .then(res => {
        if (!res.ok) throw new Error("Не удалось загрузить книги");
        return res.json();
      })
      .then(books => {
        booksContainer.innerHTML = "";
        books.forEach(book => {
          const div = document.createElement("div");
          div.className = "book";
          div.innerHTML = `<b>${book.title}</b> — ${book.author}`;
          booksContainer.appendChild(div);
        });
      })
      .catch(err => {
        booksContainer.innerHTML = `<p style="color:red">${err.message}</p>`;
      });
  }
});

