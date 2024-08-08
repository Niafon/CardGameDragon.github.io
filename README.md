<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tavern Card Game</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'MedievalSharp', cursive;
            background-color: #2c1e1e;
            color: #f1d6ab;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-image: url('https://i.imgur.com/ZWnhX4p.jpg');
            background-size: cover;
            background-position: center;
        }
        .container {
            background-color: rgba(44, 30, 30, 0.9);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            max-width: 800px;
            width: 100%;
        }
        h1, h2 {
            text-align: center;
            color: #ffd700;
        }
        button {
            background-color: #8b4513;
            color: #f1d6ab;
            border: none;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 5px;
            cursor: pointer;
            font-family: 'MedievalSharp', cursive;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #a0522d;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            background-color: rgba(139, 69, 19, 0.3);
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
        }
        .card {
            display: inline-block;
            width: 150px;
            height: 200px;
            background-color: #4e3f3f;
            border-radius: 10px;
            margin: 10px;
            padding: 10px;
            text-align: center;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s;
        }
        .card:hover {
            transform: scale(1.05);
        }
        .card-name {
            font-weight: bold;
            font-size: 1.2em;
            margin-bottom: 5px;
        }
        .card-rarity {
            font-style: italic;
        }
        .card-grade {
            font-size: 1.5em;
            font-weight: bold;
            margin-top: 10px;
        }

        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.4);
        }

        .modal-content {
            background-color: #4e3f3f;
            margin: 15% auto;
            padding: 20px;
            border: 1px solid #8b4513;
            width: 60%;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            text-align: center;
        }

        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }

        .close:hover,
        .close:focus {
            color: #f1d6ab;
            text-decoration: none;
            cursor: pointer;
        }

        .card-reveal:hover .card-reveal-inner {
            transform: rotateY(180deg);
        }

        .card-glow {
            animation: glow 1.5s ease-in-out infinite alternate;
        }

        @keyframes glow {
            from {
                box-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #fff, 0 0 20px #ff00de, 0 0 35px #ff00de, 0 0 40px #ff00de, 0 0 50px #ff00de, 0 0 75px #ff00de;
            }
            to {
                box-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #fff, 0 0 40px #ff00de, 0 0 70px #ff00de, 0 0 80px #ff00de, 0 0 100px #ff00de, 0 0 150px #ff00de;
            }
        }

        .card-reveal {
            width: 150px;
            height: 200px;
            background-color: #2c1e1e;
            margin: 10px;
            display: inline-block;
            border-radius: 10px;
            perspective: 1000px;
            cursor: pointer;
        }

        .card-reveal-inner {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.6s;
            transform-style: preserve-3d;
        }

        .card-reveal.flipped .card-reveal-inner {
            transform: rotateY(180deg);
        }

        .card-reveal-front, .card-reveal-back {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
        }

        .card-reveal-front {
            background-color: #8b4513;
            color: #f1d6ab;
            font-size: 24px;
        }

        .card-reveal-back {
            background-color: #4e3f3f;
            color: #f1d6ab;
            transform: rotateY(180deg);
        }

        .card-image-container {
            width: 100px;
            height: 70px;
            margin-bottom: 10px;
        }

        .card-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 5px;
        }

        .card-name, .card-rarity, .card-grade {
            margin: 5px 0;
        }

        .close-pack {
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #8b4513;
            color: #f1d6ab;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-family: 'MedievalSharp', cursive;
            transition: background-color 0.3s;
        }

        .close-pack:hover {
            background-color: #a0522d;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Tavern Card Game</h1>
        <p>Coins: <span id="coins">{{ user.coins }}</span></p>
        <button onclick="buyPack()">Buy Pack (100 coins)</button>
        <h2>Your Collection</h2>
        <div id="collection">
            {% for card in user.collection %}
            <div class="card">
                <div class="card-image-container">
                    <img class="card-image" src="{{ card.image_url if card.image_url else 'https://via.placeholder.com/120x80.png?text=No+Image' }}" alt="{{ card.name }}">
                </div>
                <div class="card-name">{{ card.name }}</div>
                <div class="card-rarity">{{ card.rarity }}</div>
                <div class="card-grade">{{ card.grade }}</div>
                <button onclick="marketSell('{{ card.name }}')">Sell on Market</button>
            </div>
            {% endfor %}
        </div>
        <h2>Market</h2>
        <div id="market">
            {% for item in market %}
            <div class="card">
                <div class="card-image-container">
                    <img class="card-image" src="{{ item.card.image_url if item.card.image_url else 'https://via.placeholder.com/120x80.png?text=No+Image' }}" alt="{{ item.card.name }}">
                </div>
                <div class="card-name">{{ item.card.name }}</div>
                <div class="card-rarity">{{ item.card.rarity }}</div>
                <div class="card-grade">{{ item.card.grade }}</div>
                <div>Price: {{ item.price }}</div>
               <button onclick="marketBuy('{{ item.card.name }}', {{ item.price }})">Buy</button>
            </div>
            {% endfor %}
        </div>
    </div>

    <script>
        let sellCardNameGlobal = '';
        let buyCardNameGlobal = '';

        function buyPack() {
            $.get('/buy_pack', function(data) {
                if (data.success) {
                    showBuyPackModal(data.new_cards);
                } else {
                    alert(data.message);
                }
            });
        }

        function showBuyPackModal(cards) {
            const modal = document.getElementById('buyPackModal');
            const newCardsDiv = document.getElementById('newCards');
            newCardsDiv.innerHTML = '';

            cards.forEach(card => {
                const cardDiv = document.createElement('div');
                cardDiv.className = 'card-reveal';
                cardDiv.innerHTML = `
                    <div class="card-reveal-inner">
                        <div class="card-reveal-front">?</div>
                        <div class="card-reveal-back">
                            <div class="card-image-container">
                                <img class="card-image" src="${card.image_url || 'https://via.placeholder.com/100x70.png?text=No+Image'}" alt="${card.name}">
                            </div>
                            <div class="card-name">${card.name}</div>
                            <div class="card-rarity">${card.rarity}</div>
                            <div class="card-grade">${card.grade}</div>
                        </div>
                    </div>
                `;
                newCardsDiv.appendChild(cardDiv);

                setTimeout(() => {
                    cardDiv.classList.add('card-glow');
                    cardDiv.style.boxShadow = getGlowColor(card.rarity);
                }, 500);

                cardDiv.addEventListener('click', function() {
                    this.classList.toggle('flipped');
                });
            });

            const closeButton = document.createElement('button');
            closeButton.className = 'close-pack';
            closeButton.textContent = 'Close';
            closeButton.onclick = function() {
                modal.style.display = 'none';
                location.reload();  // Перезагрузка страницы для обновления коллекции
            };
            newCardsDiv.appendChild(closeButton);

            modal.style.display = 'block';
        }

        function getGlowColor(rarity) {
            switch(rarity) {
                case 'Common': return '0 0 10px #ffffff';
                case 'Rare': return '0 0 10px #0099ff';
                case 'Epic': return '0 0 10px #9900cc';
                case 'Legendary': return '0 0 10px #ffcc00';
                default: return '0 0 10px #ffffff';
            }
        }

        function marketSell(cardName) {
            sellCardNameGlobal = cardName;
            document.getElementById('sellCardName').textContent = cardName;
            document.getElementById('sellModal').style.display = 'block';
        }

        function confirmSell() {
            const price = document.getElementById('sellPrice').value;
            $.post('/market_sell', {card_name: sellCardNameGlobal, price: price}, function(data) {
                if (data.success) {
                    alert('Card put on market!');
                    location.reload();
                } else {
                    alert(data.message);
                }
            });
            document.getElementById('sellModal').style.display = 'none';
        }

        function marketBuy(cardName, price) {
            buyCardNameGlobal = cardName;
            document.getElementById('buyCardName').textContent = cardName;
            document.getElementById('buyCardPrice').textContent = price;
            document.getElementById('buyModal').style.display = 'block';
        }

        function confirmBuy() {
            $.post('/market_buy', {card_name: buyCardNameGlobal}, function(data) {
                if (data.success) {
                    alert('Card bought from market!');
                    location.reload();
                } else {
                    alert(data.message);
                }
            });
            document.getElementById('buyModal').style.display = 'none';
        }

        function openTab(evt, tabName) {
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tabcontent");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }
            tablinks = document.getElementsByClassName("tablinks");
            for (i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        }

        // Get the element with id="defaultOpen" and click on it
        document.getElementById("defaultOpen").click();

        // Close modal when clicking on X or outside the modal
        window.onclick = function(event) {
            if (event.target.className === 'modal' || event.target.className === 'close') {
                event.target.closest('.modal').style.display = 'none';
            }
}
    </script>
        <div id="buyPackModal" class="modal">
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>Your New Cards!</h2>
                <div id="newCards"></div>
            </div>
        </div>

        <div id="sellModal" class="modal">
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>Sell Card</h2>
                <p>Enter the price for <span id="sellCardName"></span>:</p>
                <input type="number" id="sellPrice" min="1">
                <button onclick="confirmSell()">Confirm</button>
            </div>
        </div>

        <div id="buyModal" class="modal">
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>Buy Card</h2>
                <p>Are you sure you want to buy <span id="buyCardName"></span> for <span id="buyCardPrice"></span> coins?</p>
                <button onclick="confirmBuy()">Confirm</button>
            </div>
        </div>
</body>
</html>
