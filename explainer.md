# BTCScan
BTCScan is an experimental Bitcoin transaction explorer that intends to explore possible ways to present Bitcoin transaction data in a simple yet meaningful way for consumption by inexperienced Bitcoin users.


## Challenge
Despite the Bitcoin protocol being an exciting and disruptive technology that has the potential to change the lives of many, it has a few challenges to be adopted by the mainstream market. One such is understanding the transaction. Often bitcoin users are greeted with explorers that provide comprehensive and extensive information, but typically not meaningful information, especially to the general users.


## Design Philosphy & UX Consideration
BTCScan aimed to reduce cognitive load and minimize confusion by providing only relevant information in a digestible manner. The idea is the lesser, the better. It also aims to emulate UI that is familiar to the users, e.g. digital wallet transactions.

The identified key pieces of information are, in the order of priority
- Transaction Amount (total)
- Transaction Status - Confirmed or pending, and how long
- Fee incurred
- Date & Time
- Transaction ID

There are several UI/UX Techniques were implemented to create a hierarchy of information that ensured users were intuitively guided to key information, and led them through other priority-based information.

- A single card at the center of the screen unsure user's eyeballs were lead to the card.
- Enlarge transaction amount in a box at the top resulting in it being the first information user consumes. 
- Color-coded icons and text of transaction status provide instant comprehension of the state of the transaction with no cognitive load attempting to locate it
- Should the transaction is pending, it will attempt to estimate the time required for the transaction based on the network condition
- The structured layout of secondary information (txid, fee, date & time) allow users to glance through quickly and pick up the information as needed.
- A simple text sentence describing the summary of the transaction helps users to gain a better understanding of the the transaction
- Should the transaction is in confirming state, recommendation of available options are provided to the users
- As a stepping stone for users looking to learn more about Bitcoin transaction a collapsed “more information” section with advanced details are available to the user with one click. This was intentionally hidden to prevent confusing the general users.


## Backend Development
To rapidly develop a fast, testable, maintainable web application, Python with Django was picked for the task. The backend is designed and developed in such a way that it is loosely coupled
- Mempool - Responsible for configuring multiple mempools,  interacting with the mempools, and merging the mempool transactions
- Estimator - Responsible for estimating the time-to-confirmation of an unconfirmed transaction
- Transaction - Representation of a transaction as well as methods like transaction describer
- Common utilities - Collection of common utilities e.g. request for json_rpc and HTTP request, crypto utilities like shorten has, Sat/BTC conversion


## Algorithm
While several transaction prediction models exist, including Bitcoin Core's estimation algorithm and AI-based learning algorithms, considering the target audience is novice users, we determined that a prediction model based on real-time network conditions would be most suitable. The model is not only simpler to implement but also provides improved accuracy in predicting local fluctuations due to its real-time network basis.
- Retrieve unconfirmed transactions from the mempools
- Compute the fee rate (fee to virtual size ratio) for each transaction.
- Sort the transactions in descending order of their calculated fee rates.
- Group the sorted transactions into "buckets", each adhering to a 4,000,000 weight unit limit and having a distinct fee rate range.
- Predict the confirmation time of a transaction by identifying the bucket containing the transaction's fee rate within its range, with the bucket's sequence position
- Considering the average block time is ~10 minutes, the estimated time-to-confirmation would be (block position x 10 minutes).


## Front-end Development
As the user interface design revolves around clarity and responsiveness, the front end was developed with the Django template, with Tailwind CSS & Javascript. This combination greatly reduced the complexity of development and made use of the powerful templating engine provided by Django. Various key information was translated into a human-friendly format elegantly with various custom template tags.

Tailwind provided intuitive and powerful utility classes to that our web application is not only aesthetically pleasing but also accessible across different devices & screen sizes providing users with a seamless experience.


## Testing and Validation
Test cases were developed to cover major logic components to verify the functionality of these components as well as ensure maintainability and scalability.

## Improvement
During the development, server potential improvements were identified and documented as Todo for future development.
- Estimator: To handle edge cases for potentially out-of-bound fee-rate. While given the huge dataset from mempools, the risk of this edge case is low, it can be easily mitigated.
- Mempool: To ensure sufficiently large datasets are used to predict time to confirmation to improve accuracy, pulling mempool transactions synchronously can take up a significant amount of time. Supporting asynchronous jsonrpc requests can greatly reduce the total time required.
- Feature Detection: To detect feature of transactions (RBF, CPFP) to provide only relevant recommendation 
- View: Consider refactoring view.html as it gets over broad


