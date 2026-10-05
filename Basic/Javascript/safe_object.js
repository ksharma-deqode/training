function getValue(obj, key, defaultValue) {
    try {
        let val = obj[key];

        if (val == null)
            throw new Error()

        if (val == undefined)
            throw new Error()

        return val;
    } catch (error) {
        return defaultValue
    }
}


let person = {
    "name": "John",
    "city": "Indore",
}

console.log(getValue(person, "name", "Person 1"));
console.log(getValue(person, "city", "Earth"));
console.log(getValue(person, "age", "18"));


