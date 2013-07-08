package main

import "fmt"
import "io/ioutil"
import "net/http"


func main() {
    linesURL:= string("http://www.bursa.bel.tr/mobil/json.php?islem=hatlar")
    resp, err := http.Get(linesURL)
    if err != nil {
        fmt.Printf("Error occurred.")
    }
    defer resp.Body.Close()
    body, err := ioutil.ReadAll(resp.Body)
    fmt.Printf(string(body))
}

