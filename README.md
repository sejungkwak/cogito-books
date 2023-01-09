# Cogito Books

_Cogito Books_ is a fictional B2C online bookstore. The site will be targeted towards people who are interested in reading and buying books. It provides an easy-to-use interface where a user can easily find a book by filtering or searching, and make a purchase with or without registration.

The main goal of this project is to demonstrate my full-stack knowledge(HTML, CSS, JavaScript, Python/Django, relational database and Stripe payments) in a real-world context.

### View the live project [here](https://cogitobooks.herokuapp.com/)

__Note__: The site is for educational purposes only. To simulate a payment, please use a _Stripe_ test card number 4242 4242 4242 4242 with any three-digit CVC and a valid future date.

<br>

# Table of Contents

[User Experience (UX)](#user-experience-ux)
- [Website Goals](#website-goals)
- [User Stories](#user-stories)
- [Design](#design)

<br>

# User Experience (UX)

## Website Goals
- To create an online bookstore that inspires users to read books. 
- To allow users to easily find a book and make a purchase.

## User Stories

- Epic: Viewing and Navigation

    | ID | Story |
    | --- | --- |
    | [#1](https://github.com/sejungkwak/cogito-books/issues/1) | As a first-time visitor, I want to know what the shop sells immediately so that I can decide whether I will browse further. |
    | [#2](https://github.com/sejungkwak/cogito-books/issues/2) | As a first-time visitor, I want to navigate pages easily so that I can find information I’m looking for. |
    | [#3](https://github.com/sejungkwak/cogito-books/issues/3) | As a shopper, I want to know if the shop is trustworthy so that I can make a purchase without any worry. |

- Epic: Registration and User Accounts

    | ID | Story |
    | --- | --- |
    | [#4](https://github.com/sejungkwak/cogito-books/issues/4) | As a site user, I want to sign up so that I can save and view my details. |
    | [#5](https://github.com/sejungkwak/cogito-books/issues/5) | As a site user, I want to sign in and sign out of my account with my credentials so that I can keep my account secure. |
    | [#6](https://github.com/sejungkwak/cogito-books/issues/6) | As a site user, I want to update my password so that I can keep my account secure. |
    | [#7](https://github.com/sejungkwak/cogito-books/issues/7) | As a site user, I want to reset my password so that I can access my account even if I forget my password. |
    | [#8](https://github.com/sejungkwak/cogito-books/issues/8) | As a site user, I want to save my delivery information so that I don’t have to fill in the form every time I make a purchase. |
    | [#9](https://github.com/sejungkwak/cogito-books/issues/9) | As a site user, I want to update my delivery information so that I can keep my details up to date. |
    | [#10](https://github.com/sejungkwak/cogito-books/issues/10) | As a site user, I want to have a personalised user profile so that I can view my loyalty points and order history. |
    | [#11](https://github.com/sejungkwak/cogito-books/issues/11) | As a site user, I want to add books to my wishlist so that I can purchase them at a later time. |
    | [#12](https://github.com/sejungkwak/cogito-books/issues/12) | As a site user, I want to sign up for a newsletter so that I can receive regular updates about new books and offers. |

- Epic: Sorting and Searching

    | ID | Story |
    | --- | --- |
    | [#13](https://github.com/sejungkwak/cogito-books/issues/13) | As a shopper, I want to sort all the available books by publishing date so that I can easily identify newly released books. |
    | [#14](https://github.com/sejungkwak/cogito-books/issues/14) | As a shopper, I want to sort sci-fi books by user ratings so that I can easily identify the best rated books in sci-fi. |
    | [#15](https://github.com/sejungkwak/cogito-books/issues/15) | As a shopper, I want to search for a book by title so that I can easily find a book I’d like to purchase. |

- Epic: Book Reviews

    | ID | Story |
    | --- | --- |
    | [#16](https://github.com/sejungkwak/cogito-books/issues/16) | As a shopper, I want to view reviews of a book so that I can check what other people think of it. |
    | [#17](https://github.com/sejungkwak/cogito-books/issues/17) | As a shopper, I want to add a review so that I can share my thoughts. |
    | [#18](https://github.com/sejungkwak/cogito-books/issues/18) | As a shopper, I want to leave a rating without writing a review so that I can leave my opinion anonymously. | 
    | [#19](https://github.com/sejungkwak/cogito-books/issues/19) | As a shopper, I want to update my review so that I can change any incorrect information. |
    | [#20](https://github.com/sejungkwak/cogito-books/issues/20) | As a shopper, I want to remove my review so that I can delete an invalid or irrelevant review. |

- Epic: Purchasing and Checkout

    | ID | Story |
    | --- | --- |
    | [#21](https://github.com/sejungkwak/cogito-books/issues/21) | As a shopper, I want to add books to my basket while viewing multiple books at a time so that I can make my purchase as quickly and easily as possible. |
    | [#22](https://github.com/sejungkwak/cogito-books/issues/22) | As a shopper, I want to view items in my basket to be purchased so that I can identify the total cost of my purchase and all items I will receive. |
    | [#23](https://github.com/sejungkwak/cogito-books/issues/23) | As a shopper, I want to remove or adjust the quantity of individual items in my basket so that I can easily make changes to my purchase before checkout. |
    | [#24](https://github.com/sejungkwak/cogito-books/issues/24) | As a shopper, I want to easily enter my payment information so that I can check out quickly and with little hassle. |
    | [#25](https://github.com/sejungkwak/cogito-books/issues/25) | As a shopper, I want to collect loyalty points so that I can use it to purchase books. |
    | [#26](https://github.com/sejungkwak/cogito-books/issues/26) | As a shopper, I want to feel my personal and payment information are safe and secure so that I can confidently provide the needed information to make a purchase. |
    | [#27](https://github.com/sejungkwak/cogito-books/issues/27) | As a shopper, I want to view an order confirmation after checkout so that I can verify that I haven't made any mistakes. |
    | [#28](https://github.com/sejungkwak/cogito-books/issues/28) | As a shopper, I want to receive an email confirmation after checking out so that I can keep it as an invoice of what I've purchased for my records. |

- Epic: Help Centre

    | ID | Story |
    | --- | --- |
    | [#29](https://github.com/sejungkwak/cogito-books/issues/29) | As a shopper, I want to see FAQs so that I don’t have to contact the store and wait for them to respond. |
    | [#30](https://github.com/sejungkwak/cogito-books/issues/30) | As a shopper, I want to contact the store so that I can receive answers to my queries before purchase. |
    | [#31](https://github.com/sejungkwak/cogito-books/issues/31) | As a shopper, I want to receive notification via email so that I can the store answers my queries so that I can conveniently check it. |
    | [#32](https://github.com/sejungkwak/cogito-books/issues/32) | As a store owner, I want to receive notifications upon a shopper’s contact so that I can reply in a timely manner. |

- Epic: Admin and Store Management

    | ID | Story |
    | --- | --- |
    | [#33](https://github.com/sejungkwak/cogito-books/issues/33) | As a store owner, I want to add new products to my store so that I can ensure there is always something of interest to new and existing shoppers. |
    | [#34](https://github.com/sejungkwak/cogito-books/issues/34) | As a store owner, I want to update product details such as prices, description, images and so on so that I can keep the product details up to date. |
    | [#35](https://github.com/sejungkwak/cogito-books/issues/35) | As a store owner, I want to delete a product so that I can remove items that are no longer for sale. |

## Design

- Colour Scheme

    The main colours are black and white to enhance readability. Blue is added to particular elements such as buttons and notifications where information needs to grab the user’s attention.

- Typography

    [Montserrat](https://fonts.google.com/specimen/Montserrat) is the main font used throughout the whole website with Sans Serif as the fallback font in case the font isn't imported into the browser correctly. Montserrat has a highly readable body typeface and a variety of weights and styles.

- Logo

- Favicon

[Back To **Table of Contents**](#table-of-contents)