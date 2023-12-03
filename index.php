<?php
include 'db_connection.php';
?>

<!DOCTYPE html>
<!--[if lt IE 9]><html class="no-js oldie" lang="en"> <![endif]-->
<!--[if IE 9]><html class="no-js oldie ie9" lang="en"> <![endif]-->
<!--[if (gte IE 9)|!(IE)]><!-->
<html class="no-js" lang="en">
  <!--<![endif]-->

  <head>
    <!--- basic page needs
   ================================================== -->
    <meta charset="utf-8" />
    <title>LightXpense</title>
    <meta name="description" content="" />
    <meta name="author" content="" />

    <!-- mobile specific metas
   ================================================== -->
    <meta name="viewport" content="width=device-width, initial-scale=1" />

    <!-- CSS
   ================================================== -->
    <link rel="stylesheet" href="css/base.css" />
    <link rel="stylesheet" href="css/vendor.css" />
    <link rel="stylesheet" href="css/main.css" />

    <!-- script
   ================================================== -->
    <script src="js/modernizr.js"></script>
    <script src="js/pace.min.js"></script>
    <script src="https://kit.fontawesome.com/7990f7dee1.js" crossorigin="anonymous"></script>

    <!-- favicons
	================================================== -->
    <link rel="shortcut icon" href="images/logo2.png" type="image/png" />

  </head>

  <body id="top">
    <!-- header 
   ================================================== -->
    <header id="header">
      <div class="header-logo">
        <a href="index.html">LightXpense</a>
      </div>

      <nav id="header-nav-wrap">
        <ul class="header-main-nav">
          <li class="current">
            <a class="smoothscroll" href="#home" title="home">Home</a>
          </li>
          <li><a class="smoothscroll" href="#about" title="about">About</a></li>
          <li>
            <a class="smoothscroll" href="#howitworks" title="howitworks"
              >How it works</a
            >
          </li>
          <li>
            <a class="smoothscroll" href="#download" title="download"
              >Download</a
            >
          </li>
        </ul>

        <a href="login.php" title="sign-up" class="button button-primary cta"
          >Login</a
        >
      </nav>

      <a class="header-menu-toggle" href="#"><span>Menu</span></a>
    </header>
    <!-- /header -->

    <!-- home
   ================================================== -->
    <section
      id="home"
      data-parallax="scroll"
      data-image-src="images/hero-bg.png"
      data-natural-width="3000"
      data-natural-height="2000"
    >
      <div class="overlay"></div>
      <div class="home-content">
        <div class="row contents">
          <div class="home-content-left">
            <h3 data-aos="fade-up">Welcome to LightXpense</h3>

            <h1 data-aos="fade-up">
              One click solution <br />
              to reimbursement <br />
              processing
            </h1>

            <div class="buttons" data-aos="fade-up">
              <a href="#download" class="smoothscroll button stroke">
                <span class="icon-circle-down" aria-hidden="true"></span>
                Preview
              </a>
              <a
                href="http://player.vimeo.com/video/14592941?title=0&amp;byline=0&amp;portrait=0&amp;color=39b54a"
                data-lity
                class="button stroke"
              >
                <span class="icon-play" aria-hidden="true"></span>
                Watch Video
              </a>
            </div>
          </div>

          <div class="home-image-right">
            <img
              src="images/iphone-app-470.png"
              srcset="
                images/iphone-app-470.png 1x,
                images/iphone-app-940.png 2x
              "
              data-aos="fade-up"
            />
          </div>
        </div>
      </div>
      <!-- end home-content -->

      <div class="home-scrolldown">
        <a href="#about" class="scroll-icon smoothscroll">
          <span>Scroll Down</span>
          <i class="icon-arrow-right" aria-hidden="true"></i>
        </a>
      </div>
    </section>
    <!-- end home -->

    <!-- about
    ================================================== -->
    <section id="about">
      <div class="row about-intro">
        <div class="col-four">
          <h1 class="intro-header" data-aos="fade-up">About Us</h1>
        </div>
        <div class="col-eight">
          <p align='justify' class="lead" data-aos="fade-up">
            Our journey began with the simple idea that technology could
            revolutionize the way employees interact with their expenses, making
            reimbursement a breeze. We aim to re-invent how reimbursement is
            processed and facilitate seamless integration between HR, finance
            and accounting modules while keeping costs at a minimum.
          </p>
        </div>
      </div>

      <div class="row about-features">
        <div class="features-list block-1-3 block-m-1-2 block-mob-full group">
          <div class="bgrid feature" data-aos="fade-up">
            <span class="icon"><i class="fa-solid fa-camera-retro"></i></span>

            <div class="service-content">
              <h3>Snap & Claim</h3>

              <p align='justify'>
              Simplify claims submission by only submitting one photo and increases compliance.
              </p>
            </div>
          </div>
          <!-- /bgrid -->

          <div class="bgrid feature" data-aos="fade-up">
            <span class="icon"><i class="fa-solid fa-face-smile-beam"></i></span>

            <div class="service-content">
              <h3>Convenience</h3>

              <p align='justify'>
              Enhance your financial management with integrated expense data, providing your company the flexibility to oversee spending effortlessly, anytime, and enabling employees to submit expenses conveniently from any location
              </p>
            </div>
          </div>
          <!-- /bgrid -->

          <div class="bgrid feature" data-aos="fade-up">
            <span class="icon"><i class="fa-solid fa-chart-pie"></i></span>

            <div class="service-content">
              <h3>Analytics</h3>

              <p align='justify'>
                Integrate claims submission with dashboard view, enabling managers to identify trends, assess risk, and make informed, precise decisions
              </p>
            </div>
          </div>
        </div>
        <!-- end features-list -->
      </div>
      <!-- end about-features -->
    </section>
    <!-- end about -->

    <!-- pricing
    ================================================== -->
    <section id="howitworks">
        <div class="row about-how">
            <h1 class="intro-header" data-aos="fade-up">How It Works?</h1>
    
            <div class="about-how-content" data-aos="fade-up">
              <div class="about-how-steps block-1-2 block-tab-full group">
                <div class="bgrid step" data-item="1">
                  <h3>Sign-Up</h3>
                  <p align='justify'>
                    Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa
                    quae ab illo inventore veritatis et quasi architecto beatae
                    vitae dicta sunt explicabo.
                  </p>
                </div>
    
                <div class="bgrid step" data-item="2">
                  <h3>Upload</h3>
                  <p align='justify'>
                    Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa
                    quae ab illo inventore veritatis et quasi architecto beatae
                    vitae dicta sunt explicabo.
                  </p>
                </div>
    
                <div class="bgrid step" data-item="3">
                  <h3>Create</h3>
                  <p align='justify'>
                    Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa
                    quae ab illo inventore veritatis et quasi architecto beatae
                    vitae dicta sunt explicabo.
                  </p>
                </div>
    
                <div class="bgrid step" data-item="4">
                  <h3>Publish</h3>
                  <p align='justify'>
                    Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa
                    quae ab illo inventore veritatis et quasi architecto beatae
                    vitae dicta sunt explicabo.
                  </p>
                </div>
              </div>
            </div>
            <!-- end about-how-content -->
          </div>
          <!-- end about-how -->
  
          <!-- end about-bottom-image -->
      </section>  

    <!-- download
    ================================================== -->
    <section id="download">
      <div class="row">
        <div class="col-full">
          <h1 class="intro-header" data-aos="fade-up">
            Download Our App Today!
          </h1>

          <p align='justify' class="lead" data-aos="fade-up">
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
            ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
            aliquip ex ea commodo consequat. Duis aute irure dolor in
            reprehenderit in voluptate
          </p>

          <ul class="download-badges">
            <li>
              <a href="#" title="" class="badge-appstore" data-aos="fade-up"
                >App Store</a
              >
            </li>
            <li>
              <a href="#" title="" class="badge-googleplay" data-aos="fade-up"
                >Play Store</a
              >
            </li>
          </ul>
        </div>
      </div>
    </section>
    <!-- end download -->

    <!-- footer
    ================================================== -->
    <footer>
      <div class="footer-main">
        <div class="row">
          <div class="col-three md-1-3 tab-full footer-info">
            <div class="footer-logo"></div>

            <p align='justify'>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit.
              Pellentesque in ipsum id orci porta dapibus. Vivamus magna justo,
              lacinia eget consectetur sed, convallis at tellus.
            </p>

            <ul class="footer-social-list">
              <li>
                <a href="#"><i class="fa fa-facebook-square"></i></a>
              </li>
              <li>
                <a href="#"><i class="fa fa-twitter"></i></a>
              </li>
              <li>
                <a href="#"><i class="fa fa-behance"></i></a>
              </li>
              <li>
                <a href="#"><i class="fa fa-dribbble"></i></a>
              </li>
              <li>
                <a href="#"><i class="fa fa-instagram"></i></a>
              </li>
            </ul>
          </div>
          <!-- end footer-info -->

          <div class="col-three md-1-3 tab-1-2 mob-full footer-contact">
            <h4>Contact</h4>

            <p>
              1600 Amphitheatre Parkway<br />
              Mountain View, CA <br />
              94043 US<br />
            </p>

            <p>
              someone@dazzlesite.com <br />
              Phone: (+63) 555 1212 <br />
              Fax: (+63) 555 0100
            </p>
          </div>
          <!-- end footer-contact -->

          <div class="col-two md-1-3 tab-1-2 mob-full footer-site-links">
            <h4>Site Links</h4>

            <ul class="list-links">
              <li><a href="#">Home</a></li>
              <li><a href="#">About Us</a></li>
              <li><a href="#">Blog</a></li>
              <li><a href="#">FAQ</a></li>
              <li><a href="#">Terms</a></li>
              <li><a href="#">Privacy Policy</a></li>
            </ul>
          </div>
          <!-- end footer-site-links -->

          <div class="col-four md-1-2 tab-full footer-subscribe">
            <h4>Our Newsletter</h4>

            <p>
              Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua.
            </p>

            <div class="subscribe-form">
              <form id="mc-form" class="group" novalidate="true">
                <input
                  type="email"
                  value=""
                  name="EMAIL"
                  class="email"
                  id="mc-email"
                  placeholder="Email Address"
                  required=""
                />

                <input type="submit" name="subscribe" value="Send" />

                <label for="mc-email" class="subscribe-message"></label>
              </form>
            </div>
          </div>
          <!-- end footer-subscribe -->
        </div>
        <!-- /row -->
      </div>
      <!-- end footer-main -->
      </div>
    </footer>

    <div id="preloader">
      <div id="loader"></div>
    </div>

    <!-- Java Script
    ================================================== -->
    <script src="js/jquery-2.1.3.min.js"></script>
    <script src="js/plugins.js"></script>
    <script src="js/main.js"></script>
  </body>
</html>
