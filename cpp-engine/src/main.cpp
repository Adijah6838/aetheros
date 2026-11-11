#include <iostream>
#include <httplib.h>
#include <nlohmann/json.hpp>
#include "allocator.hpp"

using json = nlohmann::json;

int main() {
    httplib::Server svr;

    svr.Post("/allocate", [](const httplib::Request& req, httplib::Response& res) {
        try {
            auto j = json::parse(req.body);
            json nodes = j["nodes"];
            json vm = j["vm"];
            std::string strategy = j["strategy"];

            std::string selected_node_id = ResourceAllocator::select_node(nodes, vm, strategy);
            
            if (selected_node_id.empty()) {
                res.status = 400;
                res.set_content(json{{"error", "No suitable node found"}}.dump(), "application/json");
                return;
            }

            res.set_content(json{{"node_id", selected_node_id}}.dump(), "application/json");
        } catch (const std::exception& e) {
            res.status = 500;
            res.set_content(json{{"error", e.what()}}.dump(), "application/json");
        }
    });

    std::cout << "🚀 AetherOS C++ Engine running on port 8080" << std::endl;
    svr.listen("0.0.0.0", 8080);
    return 0;
}