Feature: Create a Training Module

  Scenario: A trainer creates a new training module
    Given I am logged in as a trainer
    When I fill in the module form with title and description
    And I submit the form
    Then the module should be listed under my created modules
