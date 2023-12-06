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
            <a class="smoothscroll" href="#ourteam" title="ourteam"
              >Our Team</a
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
              <a href="#ourteam" class="smoothscroll button stroke">
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
        <div class="features-list block-1-4 block-m-1-2 block-mob-full group">
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
            <span class="icon"><i class="fas fa-robot"></i></span>

            <div class="service-content">
              <h3>RPA Supported</h3>

              <p align='justify'>
              RPA-supported platform is meticulously designed to seamlessly classify and extract grand totals, eliminating the need for extensive HR involvement.
              </p>
            </div>
          </div>
          <!-- /bgrid -->

          <div class="bgrid feature" data-aos="fade-up">
            <span class="icon"><i class="fa-solid fa-legal"></i></span>

            <div class="service-content">
              <h3>Chart of Account Compliance</h3>

              <p align='justify'>
              Our system derives Human Resources classifications in accordance with the Chart of Accounts (COA), ensuring a standardized approach across your organization. This alignment eliminates the need for Finance teams to conduct time-consuming reclassifications when transitioning information from HR to Finance.
              </p>
            </div>
          </div>

          <div class="bgrid feature" data-aos="fade-up">
            <span class="icon"><i class="fa-solid fa-chart-pie"></i></span>

            <div class="service-content">
              <h3>Visualisation</h3>

              <p align='justify'>
              Integrate claims submission with dashboard view, enabling managers to identify trends, assess risk, and make informed, precise decisions.
              </p>
            </div>
          </div>
          <!-- /bgrid -->

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
                    HR administrators take the initiative to create registered accounts for employees. Employees are then required to log in using the provided credentials, streamlining the process and ensuring secure access to the LightXpense platform.
                  </p>
                </div>
    
                <div class="bgrid step" data-item="2">
                  <h3>Upload</h3>
                  <p align='justify'>
                    To claim reimbursement, employees capture the essence of their transactions by taking photos of the receipts. The simplicity of the process lies in the ability to effortlessly upload these images onto the LightXpense platform.
                    This step ensures that the necessary documentation for reimbursement is promptly submitted in a convenient and user-friendly manner.
                  </p>
                </div>
    
                <div class="bgrid step" data-item="3">
                  <h3>Create</h3>
                  <p align='justify'>
                    Upon successful upload of receipts, employees can delve into the LightXpense platform to create and access detailed information related to their reimbursement claims. This includes the ability to input and review relevant details, fostering transparency and accountability in the reimbursement workflow.
                  </p>
                </div>
    
                <div class="bgrid step" data-item="4">
                  <h3>Publish</h3>
                  <p align='justify'>
                    Notifications regarding the status of reimbursement claims are automatically generated within LightXpense. A centralized dashboard facilitates the collaborative effort among employees, the HR department, and the Finance department. This shared platform allows stakeholders to publish, review, and manage claim information collectively, ensuring a streamlined and efficient process for all involved parties.
                  </p>
                </div>
              </div>
            </div>
            <!-- end about-how-content -->
          </div>
          <!-- end about-how -->
  
          <!-- end about-bottom-image -->
      </section>  

    <!-- our team
    ================================================== -->
    <section id="ourteam">
      <div class="row">
        <div class="col-full">
          <h1 class="intro-header" data-aos="fade-up">
            Our Team
          </h1>
          <div class="team">
            <div class="team-member">
                <div class="team-name">
                <img src="images/LKK.png">
                <p>Low Kah Keng</p>
              </div>
              <div class="team-name">
                <img src="images/YYW.png">
                <p>Yoon Yen Wei</p>	
              </div>
              <div class="team-name">
                <img src="images/TYX.png">
                <p>Tai Yong Xin</p>
              </div>
              <div class="team-name">
                <img src="images/AB.png">
                <p>Aarogya Banepali</p>
              </div>
              <div class="team-name">
                <img src="images/SZT.png">
              <p>Siow Zi Ting</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- end our team -->

    <!-- footer
    ================================================== -->
    <footer>
      <div class="footer-main">
        <div class="row">
          <div class="col-three md-1-3 tab-full footer-info">
            <div class="footer-logo"></div>

            <p align='justify'>
              We introduce a cutting-edge budgeted solution for corporate reimbursement processes. Our advanced system efficiently auto-classifies expenses, providing companies with a powerful dashboard for enhanced financial management and streamlined operational efficiency. Elevate your company's reimbursement workflows with LighXpense.</p>

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
              5, Jalan Universiti,<br />
              Bandar Sunway,<br />
              47500 Petaling Jaya, Selangor<br />
            </p>

            <p>
              LightXpense@gmial.com <br />
              Phone: (+60) 17-667 0996 <br />
              Fax: (+60) 18-374 0028
            </p>
          </div>
          <!-- end footer-contact -->

          <div class="col-two md-1-3 tab-1-2 mob-full footer-site-links">
            <h4>Site Links</h4>

            <ul class="list-links">
              <li><a href="#">Login</a></li>
              <li><a href="#home">Home</a></li>
              <li><a href="#about">About Us</a></li>
              <li><a href="#howitworks">How it Works</a></li>
              <li><a href="#ourteam">Our Teams</a></li>
            </ul>
          </div>
          <!-- end footer-site-links -->

          <div class="col-four md-1-2 tab-full footer-subscribe">



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
