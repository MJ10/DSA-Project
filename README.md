# Network Proxy (with LFU caching)

This repository contains code for the Project 'HTTP Network Proxy with O(1) LFU caching' for the course IT204 - Data Structures and Algorithms. 

The primary objective of the project is to implement the data structure described in [this paper](http://dhruvbird.com/lfu.pdf) that allows O(1) runtime for LFU cache operations. We then use this data structure to implement LFU caching in a simple HTTP Network Proxy.

## Usage
* To start the proxy server execute the following command:
```bash
python3 main.py
```
This will start the proxy server on port 1337 (Can be edited in the main.py file)
* Go to your respective browser's proxy settings and set the HTTP proxy to `localhost` on port `1337`

## Team
* [Moksh Jain](https://github.com/MJ10), 16IT221
* [Suyash Ghuge](https://github.com/nishanthebbar2011), 16IT114
* [Nishanth Hebbar](https://github.com/suyash0103), 16IT234
* [Abhishek Kamal](https://github.com/abhishek371), 16IT202

## Contributing 
Follow the [Contributing Guidelines](https://github.com/MJ10/DSA-Project/blob/master/CONTRIBUTING.md)

## License
This repository is licensed under the [MIT License](https://github.com/MJ10/DSA-Project/blob/master/LICENSE.md)