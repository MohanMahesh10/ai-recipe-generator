let ingredients = [];

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        addIngredient();
    }
}

function addIngredient() {
    const input = document.getElementById('ingredient-input');
    const ingredient = input.value.trim();
    
    if (ingredient && !ingredients.includes(ingredient)) {
        ingredients.push(ingredient);
        updateIngredientsList();
        input.value = '';
    } else if (ingredients.includes(ingredient)) {
        showToast('This ingredient is already in your list!');
    }
}

function removeIngredient(ingredient) {
    ingredients = ingredients.filter(item => item !== ingredient);
    updateIngredientsList();
}

function updateIngredientsList() {
    const list = document.getElementById('ingredients-list');
    list.innerHTML = '';
    
    ingredients.forEach(ingredient => {
        const li = document.createElement('li');
        li.className = 'ingredient-item';
        li.innerHTML = `
            <span><i class="fas fa-check"></i> ${ingredient}</span>
            <span class="remove-btn" onclick="removeIngredient('${ingredient}')">
                <i class="fas fa-times"></i>
            </span>
        `;
        list.appendChild(li);
    });
}

function showToast(message) {
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        document.body.appendChild(toastContainer);
    }

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

function generateRecipe() {
    if (ingredients.length === 0) {
        showToast('Please add at least one ingredient!');
        return;
    }

    const loadingDiv = document.getElementById('loading');
    const recipeDiv = document.getElementById('recipe-result');
    
    loadingDiv.classList.remove('hidden');
    recipeDiv.classList.add('hidden');

    const dietary_preferences = document.getElementById('dietary-preferences').value;
    
    fetch('/generate_recipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            ingredients: ingredients,
            dietary_preferences: dietary_preferences
        })
    })
    .then(response => response.json())
    .then(data => {
        loadingDiv.classList.add('hidden');
        displayRecipe(data);
    })
    .catch(error => {
        loadingDiv.classList.add('hidden');
        console.error('Error:', error);
        showToast('Failed to generate recipe. Please try again.');
    });
}

function displayRecipe(recipe) {
    const recipeDiv = document.getElementById('recipe-result');
    recipeDiv.classList.remove('hidden');
    
    recipeDiv.innerHTML = `
        <h2><i class="fas fa-clipboard-list"></i> ${recipe.name}</h2>
        
        <div class="recipe-section">
            <h3><i class="fas fa-shopping-basket"></i> Ingredients</h3>
            <ul>
                ${recipe.ingredients.map(ing => `
                    <li><i class="fas fa-check-circle"></i> ${ing}</li>
                `).join('')}
            </ul>
        </div>

        <div class="recipe-section">
            <h3><i class="fas fa-list-ol"></i> Instructions</h3>
            <ol>
                ${recipe.instructions.map(step => `
                    <li>${step}</li>
                `).join('')}
            </ol>
        </div>

        <div class="recipe-section">
            <h3><i class="fas fa-chart-pie"></i> Nutrition Information</h3>
            <div class="nutrition-grid">
                <div class="nutrition-item">
                    <i class="fas fa-fire"></i>
                    <h4>Calories</h4>
                    <p>${recipe.nutrition.calories}</p>
                </div>
                <div class="nutrition-item">
                    <i class="fas fa-drumstick-bite"></i>
                    <h4>Protein</h4>
                    <p>${recipe.nutrition.protein}</p>
                </div>
                <div class="nutrition-item">
                    <i class="fas fa-bread-slice"></i>
                    <h4>Carbs</h4>
                    <p>${recipe.nutrition.carbs}</p>
                </div>
                <div class="nutrition-item">
                    <i class="fas fa-cheese"></i>
                    <h4>Fat</h4>
                    <p>${recipe.nutrition.fat}</p>
                </div>
            </div>
        </div>
    `;

    // Scroll to recipe
    recipeDiv.scrollIntoView({ behavior: 'smooth' });
} 