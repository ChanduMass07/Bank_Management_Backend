// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyDi2VQRdGRqYG3l-BCks54Q1Y7DJxI5OHw",
    authDomain: "bank-app-1f2f4.firebaseapp.com",
    projectId: "bank-app-1f2f4",
    storageBucket: "bank-app-1f2f4.appspot.com",
    messagingSenderId: "815393510851",
    appId: "1:815393510851:web:6fe52fb942657653e85976",
    measurementId: "G-MMTZHLBV0Q"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// ReCAPTCHA Setup
window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier("recaptcha-container", {
    size: "normal",
    callback: function(response) {
        console.log("ReCAPTCHA solved");
    },
    "expired-callback": function() {
        console.log("ReCAPTCHA expired");
    }
});

// OTP Sending Function
document.getElementById("sendOtp").addEventListener("click", function() {
    const phoneNumber = document.getElementById("phone").value.trim();
    if (!/^\d{10}$/.test(phoneNumber)) {
        alert("Enter a valid 10-digit phone number.");
        return;
    }

    const appVerifier = window.recaptchaVerifier;
    firebase.auth().signInWithPhoneNumber("+91" + phoneNumber, appVerifier)
        .then(confirmationResult => {
            window.confirmationResult = confirmationResult;
            alert("OTP Sent! Check your phone.");
        }).catch(error => {
            console.error(error);
            alert("Failed to send OTP.");
        });
});

// OTP Verification Function
document.getElementById("verifyOtp").addEventListener("click", function() {
    const otp = document.getElementById("otp").value.trim();
    if (!otp) {
        alert("Please enter the OTP.");
        return;
    }

    window.confirmationResult.confirm(otp)
        .then(result => {
            alert("Phone number verified!");
            document.getElementById("otp_verified").value = "true";
        }).catch(error => {
            console.error(error);
            alert("Invalid OTP. Please try again.");
        });
});

// Form Validation
document.getElementById("registerForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const firstName = document.getElementById("first-name").value.trim();
    const lastName = document.getElementById("last-name").value.trim();
    const fatherName = document.getElementById("father-name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirmPassword = document.getElementById("confirm-password").value.trim();
    const profilePhoto = document.getElementById("profile-photo").files[0];
    const otpVerified = document.getElementById("otp_verified").value;

    if (firstName.length < 3 || lastName.length < 3) {
        alert("Name must be at least 3 characters.");
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return;
    }

    if (password.length < 6) {
        alert("Password must be at least 6 characters long.");
        return;
    }

    if (!profilePhoto) {
        alert("Please upload a profile photo.");
        return;
    }

    if (phone.length !== 10) {
        alert("Enter a valid 10-digit phone number.");
        return;
    }

    if (otpVerified !== "true") {
        alert("Please verify your phone number first.");
        return;
    }

    alert("Registration Successful!");
    this.submit();
});
