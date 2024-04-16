document.addEventListener("DOMContentLoaded", function () {
  // toggle between pages on the user's profile
  document.querySelectorAll(".viewSwitch").forEach((element) => {
    element.onclick = function () {
      load_view(this.dataset.page);
    };
  });

  // edit/save post button
  document.querySelectorAll(".edit-btn").forEach((btn) => {
    btn.onclick = function () {
      edit_post(this.dataset.editbtn);
    };
  });

  //like post button
  document.querySelectorAll(".like-btn").forEach((btn) => {
    btn.onclick = function () {
      like_post(this.dataset.likebtn);
      console.log(this.dataset.likebtn);
    };
  });

  //default load view
  let elemProfileView = document.querySelector("#profile-posts");
  if (elemProfileView) {
    load_view("profile-posts");
  }
});

// load function
function load_view(view) {
  document.querySelectorAll(".view").forEach((view) => {
    view.style.display = "none";
  });
  document.querySelectorAll("[data-page]").forEach((page) => {
    page.style.borderBottom = "none";
  });

  document.querySelector(`#${view}`).style.display = "block";
  document.querySelector(`[data-page=${view}]`).style.borderBottom =
    "4px solid #007bff";
}

// edit post function
function edit_post(id) {
  let actionBtn = document.querySelector(`#btn${id}`);
  let postText = document.getElementById(id);
  let div = document.querySelector(`#div${id}`);
  if (actionBtn.textContent === "Edit Post") {
    let textarea = document.createElement("textarea");
    textarea.style.width = "100%";
    textarea.style.padding = "5px 10px";
    div.insertBefore(textarea, postText);
    textarea.innerHTML = postText.innerHTML;

    postText.style.display = "none";
    actionBtn.innerHTML = "Save Post";
    actionBtn.type = "button";
  } else if (actionBtn.textContent === "Save Post") {
    actionBtn.type = "submit";
    let textarea = document.querySelector("textarea");
    postText.innerHTML = textarea.value;
    postText.style.display = "block";
    textarea.remove();
    actionBtn.innerHTML = "Edit Post";

    fetch(`/editPost/${id}`, {
      method: "PUT",
      body: JSON.stringify({
        id: id,
        postText: postText.innerHTML,
      }),
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getToken("csrftoken"),
      },
    }).then(async (response) => {
      console.log(postText);
    });
  }
}

//like post function
function like_post(id) {
  let likeBtn = document.querySelector(`[data-likebtn="${id}"] i`);
  let likeCountArea = document.querySelector(`#likeCount${id}`);

  let counter = parseInt(likeCountArea.innerHTML);
  // if icon is regular and count is 0 => make icon solid and count +1
  // if user already liked the post, do unlike
  if (likeBtn.classList.contains("fa-regular")) {
    likeBtn.classList.remove("fa-regular");
    likeBtn.classList.add("fa-solid");
    counter++;
    likeCountArea.innerHTML = `${counter}`;

    fetch(`/likePost/${id}`, {
      method: "POST",
      body: JSON.stringify({
        id: id,
      }),
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getToken("csrftoken"),
      },
    }).then(async (response) => {
      console.log(response);
    });
  } else if (likeBtn.classList.contains("fa-solid")) {
    likeBtn.classList.remove("fa-solid");
    likeBtn.classList.add("fa-regular");
    counter--;
    likeCountArea.innerHTML = `${counter}`;
    console.log(`${id}`);
    fetch(`/likePost/${id}`, {
      method: "PUT",
      body: JSON.stringify({
        id: id,
      }),
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getToken("csrftoken"),
      },
    }).then(async (response) => {
      console.log(response);
    });
  }
  console.log(likeBtn);
}

// get token function
function getToken(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie != "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
