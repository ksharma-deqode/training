function executeWithContext(obj, fn){
    return fn.call(obj)
}

const person = {
    name: "John",
    age: 25
}

function hello(name){
    return ("Hello,", this.name);
}

const output = executeWithContext(person,hello);

console.log(output)