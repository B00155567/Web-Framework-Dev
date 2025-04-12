Feature: Track Progress

  Scenario: A trainee views progress on a module
    Given I am logged in as a trainee
    When I visit the module dashboard
    Then I should see my completion percentage and last accessed date
