"use strict";

const logInButton = document.getElementById("log-in");
const loginPopup = document.getElementById("popup-form");
const loginForm = document.getElementById("login-form");

const signUpForm = document.getElementById("sign-up-form");
const signUpLink = document.getElementById("sign-up-link");

const addTopicButton = document.getElementById("add-topic-button");
const addTopicPopup = document.getElementById("add-topic-popup");
const addTopicForm = document.getElementById("add-topic-form");

const addClaimButton = document.getElementById("add-claim-button");
const addClaimPopup = document.getElementById("add-claim-popup");
const addClaimForm = document.getElementById("add-claim-form");

const addReplyButton = document.getElementById("add-reply-button");
const addReplyPopup = document.getElementById("add-reply-popup");
const addReplyForm = document.getElementById("add-reply-form");

const addReplyToReplyButton = document.getElementById("add-reply-to-reply-button");
const addReplyToReplyPopUp = document.getElementById("add-reply-to-reply-popup");
const addReplyToReplyForm = document.getElementById("add-reply-to-reply-form");

// log in and sign up button
if (logInButton) {
    logInButton.addEventListener("click", function (event) {
        event.preventDefault();
        if (this.innerText === "Log Out") {
            fetch('/logout', { 
                method: 'POST' 
            })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    location.reload();
                });

        } else if (loginPopup) {
            loginPopup.style.display = "flex";
            if (signUpForm) signUpForm.style.display = "none";
            if (loginForm) loginForm.style.display = "block";
        }
    });
}

// X button closes all the pop up forms
document.querySelectorAll(".close-button").forEach(button => { // close button class (.)
    button.addEventListener("click", () => {
        if (button.closest(".popup")) {
            button.closest(".popup").style.display = "none";
        }
        // hide the log in and sign up forms when user presses "X"
        if(loginForm) loginForm.style.display = "none";
        if(signUpForm) signUpForm.style.display = "none";
    });
});

// switches to sign up
if (signUpLink) {
    signUpLink.addEventListener("click", function (event) {
        event.preventDefault();
        if (loginPopup) {
            loginPopup.style.display = "flex";
            if (loginForm) loginForm.style.display = "none";
            if (signUpForm) signUpForm.style.display = "block";
        }
    });
}

// add topic display
if (addTopicButton) {
    addTopicButton.addEventListener("click", function () {
        fetch('/checkLogin', { 
            method: 'POST' 
        })
            .then(response => response.json())
            .then(data => {
                if (!data.logged_in) {
                    alert("You have to log in");
                } else if (addTopicForm) {
                    addTopicPopup.style.display = "flex";
                }
            });
    });
}

// add topic submission  
if (addTopicForm) {
    addTopicForm.addEventListener("submit", function (event) {
        event.preventDefault();
        
        const topicName = addTopicForm.querySelector('textarea[name="topic_text"]').value.trim();

        if (!topicName) {
            alert("Enter topic name");
            return;
        }

        fetch('/add_topic', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic_name: topicName }),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.success) {
                location.reload();
            }
        });
    });
}

// add claim display
if (addClaimButton) {
    addClaimButton.addEventListener("click", function () {
        fetch('/checkLogin', { 
            method: 'POST' 
        })
            .then(response => response.json())
            .then(data => {
                if (!data.logged_in) {
                    alert("You have to log in");
                } else if (addClaimPopup) {
                    addClaimPopup.style.display = "flex";
                }
            });
    });
}

// add claim submission  
if (addClaimForm) {
    addClaimForm.addEventListener("submit", function (event) {
        event.preventDefault();
        
        const topicName = addClaimForm.querySelector('input[name="topic_name"]').value;
        const claimText = addClaimForm.querySelector('textarea[name="claim_text"]').value.trim();

        if (!topicName || !claimText) {
            alert("Fill all the blanks");
            return;
        }

        fetch('/add_claim', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic_name: topicName, claim_text: claimText }),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.success) location.reload();
        });
    });
}

// login submission 
if (loginForm) {
    const loginButton = loginForm.querySelector(".button");
    if (loginButton) {
        loginButton.addEventListener("click", function (event) {
            event.preventDefault();
            const username = loginForm.querySelector('input[type="text"]').value.trim();
            const password = loginForm.querySelector('input[type="password"]').value.trim();

            if (!username || !password) {
                alert("Enter your username and password");
                return;
            }

            fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                if (data.success) {
                    location.reload();
                }
            });
        });
    }
}

// sign up submission 
if (signUpForm) {
    const signUpButton = signUpForm.querySelector(".button");
    if (signUpButton) {
        signUpButton.addEventListener("click", function (event) {
            event.preventDefault();
            const username = signUpForm.querySelector('input[type="text"]').value.trim();
            const password = signUpForm.querySelector('input[type="password"]').value.trim();

            if (!username || !password) {
                alert("Enter your username and password");
                return;
            }

            fetch('/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                if (data.success) location.reload();
            });
        });
    }
}

// add reply display
if (addReplyButton) {
    addReplyButton.addEventListener("click", function () {
        fetch('/checkLogin', { 
            method: 'POST' 
        })
            .then(response => response.json())
            .then(data => {
                if (!data.logged_in) {
                    alert("You have to log in");
                } else if (addReplyPopup) {
                    addReplyPopup.style.display = "flex";
                }
            });
    });
}

// add reply submission  
if (addReplyForm) {
    addReplyForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const claimId = addReplyForm.querySelector('input[name="claim_id"]').value;
        const replyText = addReplyForm.querySelector('textarea[name="reply_text"]').value.trim();
        const replyType = addReplyForm.querySelector('input[name="reply_type"]:checked').value;
        
        if (!replyText || !replyType) {
            alert("Add your text or select the reply type");
            return;
        }
        fetch('/add_reply', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ claim_id: claimId, reply_text: replyText, reply_type: replyType }),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.success) {
                location.reload();
            }
        });
    });
}

// reply to reply display
document.querySelectorAll(".add-reply-to-reply-button").forEach(button => {
    button.addEventListener("click", function () {
        const parentReplyId = this.getAttribute("reply_text_id");
        document.getElementById("parent-reply-id").value = parentReplyId;

        fetch("/checkLogin", { 
            method: "POST" 
        })
            .then(response => response.json())
            .then(data => {
                if (!data.logged_in) {
                    alert("You have to log in");
                } else if (addReplyToReplyPopUp) {
                    addReplyToReplyPopUp.style.display = "flex";
                }
            });
    });
});

// reply to reply form submission
if (addReplyToReplyForm) {
    addReplyToReplyForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const replyText = addReplyToReplyForm.querySelector('textarea[name="reply_to_reply_text"]').value.trim();
        const replyType = addReplyToReplyForm.querySelector('input[name="reply_type"]:checked').value;
        const parentReplyId = document.getElementById("parent-reply-id").value; 

        if (!replyText) {
            alert("Enter text");
            return;
        }

        if (!replyType) {
            alert("Pick the reply type");
            return;
        }

        fetch("/add_reply_to_reply", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ parent_reply_id: parentReplyId, reply_to_reply_text: replyText, reply_type: replyType }),
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                if (data.success) {
                    location.reload();
                }
            });
    });
}