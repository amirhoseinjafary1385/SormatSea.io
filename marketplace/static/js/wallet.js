// Wallet Connection Manager for SormatSea.io NFT Marketplace

class WalletManager {
    constructor() {
        this.web3 = null;
        this.account = null;
        this.chainId = null;
        this.isConnected = false;
        this.supportedChainIds = {
            1: 'Ethereum Mainnet',
            3: 'Ropsten Testnet',
            4: 'Rinkeby Testnet',
            5: 'Goerli Testnet',
            56: 'BSC Mainnet',
            97: 'BSC Testnet',
            137: 'Polygon Mainnet',
            80001: 'Mumbai Testnet'
        };
        this.init();
    }

    async init() {
        // Check if wallet was previously connected
        await this.checkConnection();
        
        // Listen for account changes
        this.setupEventListeners();
        
        // Update UI
        this.updateWalletUI();
    }

    async checkConnection() {
        if (typeof window.ethereum !== 'undefined') {
            try {
                this.web3 = new Web3(window.ethereum);
                const accounts = await window.ethereum.request({ 
                    method: 'eth_accounts' 
                });
                
                if (accounts.length > 0) {
                    this.account = accounts[0];
                    this.isConnected = true;
                    this.chainId = await window.ethereum.request({ 
                        method: 'eth_chainId' 
                    });
                    await this.updateBalance();
                }
            } catch (error) {
                console.error('Error checking wallet connection:', error);
            }
        }
    }

    setupEventListeners() {
        if (typeof window.ethereum !== 'undefined') {
            // Account changed
            window.ethereum.on('accountsChanged', (accounts) => {
                if (accounts.length === 0) {
                    this.disconnect();
                } else {
                    this.account = accounts[0];
                    this.updateBalance();
                    this.updateWalletUI();
                }
            });

            // Chain changed
            window.ethereum.on('chainChanged', (chainId) => {
                this.chainId = chainId;
                this.updateWalletUI();
                // Reload page to reset dapp state
                window.location.reload();
            });

            // Connection changed
            window.ethereum.on('connect', (connectInfo) => {
                console.log('Wallet connected:', connectInfo);
            });

            // Disconnection
            window.ethereum.on('disconnect', (error) => {
                console.log('Wallet disconnected:', error);
                this.disconnect();
            });
        }
    }

    async connectWallet() {
        if (typeof window.ethereum === 'undefined') {
            this.showWalletOptions();
            return;
        }

        try {
            // Show loading state
            this.updateWalletButton('Connecting...', true);

            // Request account access
            const accounts = await window.ethereum.request({
                method: 'eth_requestAccounts'
            });

            if (accounts.length > 0) {
                this.web3 = new Web3(window.ethereum);
                this.account = accounts[0];
                this.isConnected = true;
                this.chainId = await window.ethereum.request({ 
                    method: 'eth_chainId' 
                });

                await this.updateBalance();
                this.updateWalletUI();
                this.showSuccessMessage('Wallet connected successfully!');

                // Save connection state
                localStorage.setItem('walletConnected', 'true');
                localStorage.setItem('walletAddress', this.account);

                // Dispatch custom event
                window.dispatchEvent(new CustomEvent('walletConnected', {
                    detail: { address: this.account, chainId: this.chainId }
                }));

            } else {
                throw new Error('No accounts found');
            }

        } catch (error) {
            console.error('Error connecting wallet:', error);
            this.handleWalletError(error);
        }
    }

    async updateBalance() {
        if (this.web3 && this.account) {
            try {
                const balance = await this.web3.eth.getBalance(this.account);
                this.balance = this.web3.utils.fromWei(balance, 'ether');
            } catch (error) {
                console.error('Error fetching balance:', error);
                this.balance = '0';
            }
        }
    }

    disconnect() {
        this.account = null;
        this.balance = null;
        this.isConnected = false;
        this.web3 = null;
        this.chainId = null;

        // Clear localStorage
        localStorage.removeItem('walletConnected');
        localStorage.removeItem('walletAddress');

        // Update UI
        this.updateWalletUI();
        this.showSuccessMessage('Wallet disconnected');

        // Dispatch custom event
        window.dispatchEvent(new CustomEvent('walletDisconnected'));
    }

    updateWalletUI() {
        const walletButton = document.getElementById('walletButton');
        const walletText = document.getElementById('walletText');

        if (!walletButton || !walletText) return;

        if (this.isConnected && this.account) {
            // Connected state
            walletButton.classList.add('wallet-connected');
            walletButton.onclick = () => this.showWalletInfo();
            
            const shortAddress = this.formatAddress(this.account);
            walletText.innerHTML = `
                <span class="wallet-address">${shortAddress}</span>
                ${this.balance ? `<div class="wallet-balance">${parseFloat(this.balance).toFixed(4)} ETH</div>` : ''}
            `;

            // Add network indicator
            this.addNetworkIndicator();

        } else {
            // Disconnected state
            walletButton.classList.remove('wallet-connected');
            walletButton.onclick = () => this.connectWallet();
            walletText.textContent = 'Connect Wallet';
        }
    }

    updateWalletButton(text, loading = false) {
        const walletText = document.getElementById('walletText');
        const walletButton = document.getElementById('walletButton');
        
        if (walletText) {
            walletText.textContent = text;
        }
        
        if (walletButton) {
            walletButton.disabled = loading;
            if (loading) {
                walletButton.classList.add('loading');
            } else {
                walletButton.classList.remove('loading');
            }
        }
    }

    formatAddress(address) {
        if (!address) return '';
        return `${address.substring(0, 6)}...${address.substring(address.length - 4)}`;
    }

    addNetworkIndicator() {
        const chainIdDecimal = parseInt(this.chainId, 16);
        const networkName = this.supportedChainIds[chainIdDecimal] || 'Unknown Network';
        
        // Add network badge if not exists
        let networkBadge = document.querySelector('.network-badge');
        if (!networkBadge) {
            networkBadge = document.createElement('div');
            networkBadge.className = 'network-badge';
            document.getElementById('walletButton').appendChild(networkBadge);
        }
        
        networkBadge.textContent = networkName;
        networkBadge.title = `Connected to ${networkName}`;
    }

    showWalletOptions() {
        // Create modal for wallet options
        const modal = document.createElement('div');
        modal.className = 'wallet-modal';
        modal.innerHTML = `
            <div class="wallet-modal-content">
                <div class="wallet-modal-header">
                    <h5>Connect Your Wallet</h5>
                    <button class="btn-close" onclick="this.closest('.wallet-modal').remove()"></button>
                </div>
                <div class="wallet-modal-body">
                    <div class="wallet-options">
                        <div class="wallet-option" onclick="window.open('https://metamask.io/', '_blank')">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/3/36/MetaMask_Fox.svg" 
                                 alt="MetaMask" class="wallet-icon">
                            <div>
                                <strong>MetaMask</strong>
                                <p>Connect using browser wallet</p>
                            </div>
                        </div>
                        <div class="wallet-option" onclick="window.open('https://walletconnect.com/', '_blank')">
                            <img src="https://walletconnect.com/walletconnect-logo.svg" 
                                 alt="WalletConnect" class="wallet-icon">
                            <div>
                                <strong>WalletConnect</strong>
                                <p>Connect using mobile wallet</p>
                            </div>
                        </div>
                        <div class="wallet-option" onclick="window.open('https://www.coinbase.com/wallet', '_blank')">
                            <img src="https://avatars.githubusercontent.com/u/18060234?s=280&v=4" 
                                 alt="Coinbase" class="wallet-icon">
                            <div>
                                <strong>Coinbase Wallet</strong>
                                <p>Connect using Coinbase Wallet</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        
        // Close modal when clicking outside
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }

    showWalletInfo() {
        // Create wallet info modal
        const modal = document.createElement('div');
        modal.className = 'wallet-modal';
        modal.innerHTML = `
            <div class="wallet-modal-content">
                <div class="wallet-modal-header">
                    <h5>Wallet Information</h5>
                    <button class="btn-close" onclick="this.closest('.wallet-modal').remove()"></button>
                </div>
                <div class="wallet-modal-body">
                    <div class="wallet-info">
                        <div class="info-item">
                            <label>Address:</label>
                            <div class="address-container">
                                <span class="address">${this.account}</span>
                                <button class="btn btn-sm btn-outline-primary" onclick="navigator.clipboard.writeText('${this.account}')">
                                    <i class="bi bi-clipboard"></i>
                                </button>
                            </div>
                        </div>
                        <div class="info-item">
                            <label>Balance:</label>
                            <span>${this.balance ? parseFloat(this.balance).toFixed(6) : '0'} ETH</span>
                        </div>
                        <div class="info-item">
                            <label>Network:</label>
                            <span>${this.supportedChainIds[parseInt(this.chainId, 16)] || 'Unknown'}</span>
                        </div>
                    </div>
                    <div class="wallet-actions">
                        <button class="btn btn-primary" onclick="walletManager.refreshBalance()">
                            <i class="bi bi-arrow-clockwise me-2"></i>Refresh Balance
                        </button>
                        <button class="btn btn-danger" onclick="walletManager.disconnect(); this.closest('.wallet-modal').remove()">
                            <i class="bi bi-box-arrow-right me-2"></i>Disconnect
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        
        // Close modal when clicking outside
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }

    async refreshBalance() {
        await this.updateBalance();
        this.updateWalletUI();
        this.showSuccessMessage('Balance updated');
    }

    handleWalletError(error) {
        let message = 'Failed to connect wallet';
        
        if (error.code === 4001) {
            message = 'Connection rejected by user';
        } else if (error.code === -32002) {
            message = 'Connection request already pending';
        } else if (error.message) {
            message = error.message;
        }

        this.showErrorMessage(message);
        this.updateWalletButton('Connect Wallet', false);
    }

    showSuccessMessage(message) {
        this.showToast(message, 'success');
    }

    showErrorMessage(message) {
        this.showToast(message, 'error');
    }

    showToast(message, type = 'info') {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="bi ${type === 'success' ? 'bi-check-circle' : type === 'error' ? 'bi-exclamation-circle' : 'bi-info-circle'}"></i>
                <span>${message}</span>
            </div>
        `;

        document.body.appendChild(toast);

        // Show toast
        setTimeout(() => toast.classList.add('show'), 100);

        // Remove toast after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Utility methods for NFT transactions
    async signMessage(message) {
        if (!this.web3 || !this.account) {
            throw new Error('Wallet not connected');
        }

        try {
            const signature = await this.web3.eth.personal.sign(message, this.account);
            return signature;
        } catch (error) {
            console.error('Error signing message:', error);
            throw error;
        }
    }

    async sendTransaction(transactionObject) {
        if (!this.web3 || !this.account) {
            throw new Error('Wallet not connected');
        }

        try {
            const txHash = await this.web3.eth.sendTransaction({
                from: this.account,
                ...transactionObject
            });
            return txHash;
        } catch (error) {
            console.error('Error sending transaction:', error);
            throw error;
        }
    }

    // Check if user can afford NFT
    async canAffordNFT(priceInEth) {
        if (!this.balance) {
            await this.updateBalance();
        }
        return parseFloat(this.balance) >= parseFloat(priceInEth);
    }
}

// Initialize wallet manager
let walletManager;

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    walletManager = new WalletManager();
});

// Global function for button onclick
function connectWallet() {
    if (walletManager) {
        if (walletManager.isConnected) {
            walletManager.showWalletInfo();
        } else {
            walletManager.connectWallet();
        }
    }
}


// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WalletManager;
}
