#ifndef DIV_SELECTOR_H
#define DIV_SELECTOR_H

#include <deque>
#include "./div_tiebreaking_open_list.h" // for the enums
#include <optional>
using std::deque;

template<class Entry>
class Selector {

    int counter;

    using DepthBucket = deque<Entry>;
    deque<DepthBucket> depth_bucket_list;

public:
    Selector()
        : counter(-1) {
    }

    Entry remove_next(div_tiebreaking_open_list::TieBreakingCriteria tiebreaking_criteria) {
        if (empty()) {
            std::cerr << "Selector::remove_next() called on empty Selector" << std::endl;
            exit(1);
        }

        if (counter == -1) {
            if (depth_bucket_list.empty()) {
                std::cerr << "depth_bucket_list is currently empty" << std::endl;
            } else {
                rewind_counter();
            }
        }

        // search until non-empty DepthBucket is found
        while (counter >= 0 && depth_bucket_list[counter].empty()) {
            counter--;
        }

        if (counter < 0) { // no non-empty bucket found
            std::cerr << "All DepthBuckets are currently empty" << std::endl;
            exit(1);
        }

        std::optional<Entry> result;

        switch(tiebreaking_criteria) {
            case div_tiebreaking_open_list::TieBreakingCriteria::FIFO:
                result = depth_bucket_list[counter].front(); // Tiebreaking inside DepthBucket is FIFO
                depth_bucket_list[counter].pop_front();
                break;
            case div_tiebreaking_open_list::TieBreakingCriteria::LIFO:
                result = depth_bucket_list[counter].back(); // Tiebreaking inside DepthBucket is LIFO
                depth_bucket_list[counter].pop_back();
                break;
            case div_tiebreaking_open_list::TieBreakingCriteria::RANDOM:
                // TODO
                break;
            default:
                std::cout << "Tie-breaking criteria was not found. Using default FIFO." << std::endl;
                result = depth_bucket_list[counter].front(); // Tiebreaking inside DepthBucket is FIFO
                depth_bucket_list[counter].pop_front();
        }

        decrease_counter();
        return *result;
    }

    void add(Entry entry, int d_value) {
        if (depth_bucket_list.size() <= d_value) {
            depth_bucket_list.resize(d_value + 1);
        }
        depth_bucket_list[d_value].push_back(entry);
    }

    bool empty() {
        for (const auto &bucket : depth_bucket_list) {
            if (!bucket.empty())
                return false;
        }
        return true;
    }

protected:
    void decrease_counter() {
        --counter;
        if (counter < 0) {
            rewind_counter();
        }
    }

    void rewind_counter() {
        for (int i = depth_bucket_list.size() - 1; i >= 0; --i) { // goes over all DepthBuckets and finds deepest non-empty one
            if (!depth_bucket_list[i].empty()) {
                counter = i;
                return;
            }
        }
        std::cerr << "All DepthBuckets are empty and counter = -1" << std::endl;
        counter = -1;
    }
};


#endif
