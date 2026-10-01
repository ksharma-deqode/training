function inheritsFrom(obj, constructor) {

    if (obj == null || typeof obj != 'object' && typeof obj != 'function') {
        return false;
    }
    let requiredPrototype = constructor.prototype;
    let currentPrototype = obj.__proto__;


    while (currentPrototype != null) {
        if (currentPrototype == requiredPrototype) {
            return true;
        }
        currentPrototype = currentPrototype.__proto__;
    }

    return false
}

class Animal {
    constructor(name) {
        this.name = name;
    }
}

class Dog extends Animal {
    constructor(name) {
        super(name);
        this.name = name;
    }
}

let an = new Animal("animale");
let dg = new Dog("doggy");

console.log(inheritsFrom(an, Animal));
console.log(inheritsFrom(dg, Animal));
console.log(inheritsFrom("Hello", String));