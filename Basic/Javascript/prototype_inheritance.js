class Animal {
    constructor(name) {
        this.name = name;
    }
}

Animal.prototype.speak = function () {
    return "...";
}

class Dog extends Animal {
    constructor(name) {
        super(name);
        this.name = name;
    }
}

Dog.prototype.speak = function () {
    return "Woof";
}

function createDog(name) {
    return new Dog(name);
}

let test_obj = createDog("Husky");

console.log(test_obj.name);
console.log(test_obj.speak());
