function filterWithContext(array, predicate, context) {
    let man_arr = [];

    for (let i = 0; i < array.length; i++) {
        let curr_ele = array[i];

        let isTrue = predicate.call(context, curr_ele, i, array);

        if (isTrue) {
            man_arr.push(curr_ele);
        }
    }

    return man_arr;
}

function isEven(curr_ele, index, org_arr) {

    return curr_ele % 2 == 0;
}



let arr = [5, 89, 75, 74, 76, 72, 2, 3, 12, 15, 16, 95];

let evenarr = filterWithContext(arr, predicate, null);

console.log(evenarr);
