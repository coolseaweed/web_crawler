#!/bin/bash




categories="livelihood gourmet lifestyle shopping childraising health travel pet column education reading design humanities science business career it local manga entertainment movie music radio stage game sports baseball soccer tech gadget love art creation novel photo"

for category in $categories; do
    (
        echo $category;
        scrapy crawl bot --nolog -a category=$category;
    )&
done




