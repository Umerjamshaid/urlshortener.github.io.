---

# 🚀 URL Shortener with Django

![banner](https://github.com/Umerjamshaid/urlshortener/blob/main/Screenshots/catalog.jpg)

[![Django Version](https://img.shields.io/badge/Django-4.1.13-brightgreen.svg)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/your-repo/url-shortener/pulls)
[![Build Status](https://travis-ci.com/your-username/url-shortener.svg?branch=main)](https://travis-ci.com/your-username/url-shortener)
[![codecov](https://codecov.io/gh/Umerjamshaid/url-shortener/branch/main/graph/badge.svg)](https://codecov.io/gh/Umerjamshaid/url-shortener)

## 🎯 Project Overview

Welcome to the **URL Shortener** project built with **Django**! This project allows users to shorten long URLs into compact, easy-to-share links, similar to popular services like **bit.ly**. The project includes:

- URL shortening functionality with a randomly generated short code.
- Redirection to the original URL when a short link is visited.
- YouTube video downloader for added fun!

### 🌟 Key Features

- **Shorten Long URLs**: Generate short, easy-to-share URLs with a custom short code.
- **Custom Redirects**: Visit the shortened URL to get redirected to the original.
- **YouTube Downloader**: Download YouTube videos in various resolutions (optional feature).
- **Simple API**: Easily integrate the shortener into other apps via the REST API.

---

## 📸 Screenshots

### Home Page

![Home Page](screenshots/home.png)

### Shorten URL Page

![Shorten URL Page](screenshots/about.png)

### YouTube Downloader

![YouTube Downloader](screenshots/youtube.png)

---

## 🛠️ Installation & Setup

Follow these steps to set up the project locally:

### 1. **Clone the Repository**

```bash
git clone https://github.com/your-username/url-shortener.git
cd url-shortener
```

### 2. **Set Up a Virtual Environment**

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### 3. **Install Required Dependencies**

```bash
# Install dependencies from requirements.txt
pip install -r requirements.txt
```

### 4. **Migrate the Database**

```bash
# Run database migrations
python manage.py migrate
```

### 5. **Run the Development Server**

```bash
# Start the Django development server
python manage.py runserver
```

Now, open your browser and visit **`http://127.0.0.1:8000`**. Your URL Shortener should be up and running!

---

## 🔥 Usage

### 1. **Home Page**

- This is the landing page where you can shorten URLs. Just enter a long URL, and a shortened link will be generated.

![Shorten URL Page](screenshots/home.png)

### 2. **Shortened URL**

- Once you enter a URL, the application will generate a short link. Example: **`http://127.0.0.1:8000/abc123/`**
- Share the short link, and anyone visiting it will be redirected to the original URL.

![Shortened URL](screenshots/result.png)

### 3. **YouTube Video Downloader**

- Go to the YouTube section, enter the video link, select the desired resolution, and download your video locally!

![YouTube Downloader](screenshots/youtube.png)

---

## 🧩 API Documentation

Our project also provides an API for programmatically shortening URLs. You can integrate it into other apps.

### **Endpoint: `/api/shorten/`**

- **Method**: POST
- **Request Body**:

  ```json
  {
    "original_url": "https://example.com"
  }
  ```

- **Response**:
  ```json
  {
    "short_url": "http://127.0.0.1:8000/abc123/"
  }
  ```

---

## 🛡️ Running Tests

To ensure everything is functioning as expected, run the following command:

```bash
python manage.py test
```

You can add unit tests to test various components of your project.

---

## 💻 Technologies Used

- **Python**: 3.12.4
- **Django**: 4.1.13
- **Pytube**: For YouTube video downloading
- **Bootstrap 5**: For the modern and responsive frontend

---

## 👨‍💻 Contributing

We welcome contributions! Please follow the steps below to contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgments

- Thanks to the Django community for the fantastic documentation and tutorials.
- Shout-out to **Umer Jamshaid** and **Yahya Rizwan** for building this awesome project!
- Special Thanks to **Sir Muzamil Bilwani** for his guidance and support 🫡

---

## 🏗️ Future Improvements

- **Custom Short Codes**: Allow users to specify custom short codes for their URLs.
- **User Authentication**: Add login/signup features to allow personalized URL management.
- **Analytics**: Add basic analytics to track how often a URL is clicked.
- **UI Enhancements**: Further improve the UI to enhance the user experience.

---

### Additional Badges

Here are some additional badges you can use if you configure CI/CD services like Travis CI and Codecov:

- [![Build Status](https://travis-ci.com/Umerjamshaid/url-shortener.svg?branch=main)](https://travis-ci.com/Umerjamshaid/url-shortener)
- [![codecov](https://codecov.io/gh/Umerjamshaid/url-short
